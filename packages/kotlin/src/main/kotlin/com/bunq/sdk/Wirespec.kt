@file:OptIn(ExperimentalStdlibApi::class)

package com.bunq.sdk

import com.bunq.sdk.generated.Client
import community.flock.wirespec.integration.jackson.v3.kotlin.WirespecModuleKotlin
import community.flock.wirespec.kotlin.Wirespec
import community.flock.wirespec.kotlin.Wirespec.ParamSerialization
import community.flock.wirespec.kotlin.Wirespec.PathSerialization
import community.flock.wirespec.kotlin.serde.DefaultParamSerialization
import community.flock.wirespec.kotlin.serde.DefaultPathSerialization
import io.github.oshai.kotlinlogging.KotlinLogging
import java.util.concurrent.atomic.AtomicReference
import kotlin.reflect.KType
import kotlin.reflect.javaType
import tools.jackson.databind.DeserializationFeature
import tools.jackson.databind.ObjectMapper
import tools.jackson.databind.json.JsonMapper
import tools.jackson.databind.node.ObjectNode
import tools.jackson.module.kotlin.KotlinFeature
import tools.jackson.module.kotlin.kotlinModule


private val logger = KotlinLogging.logger {}

internal val objectMapper: ObjectMapper = JsonMapper.builder()
    .configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false)
    .addModule(kotlinModule {
        enable(KotlinFeature.KotlinPropertyNameAsImplicitName)
    })
    .addModule(WirespecModuleKotlin())
    .build()


val serialization: Wirespec.Serialization =
    object : Wirespec.Serialization, ParamSerialization by DefaultParamSerialization(),
        PathSerialization by DefaultPathSerialization() {
        override fun <T : Any> serializeBody(t: T, kType: KType): ByteArray {
            if (t is Unit) return ByteArray(0)
            return objectMapper.writeValueAsBytes(t)
        }

        override fun <T : Any> deserializeBody(raw: ByteArray, kType: KType): T {
            val tree = objectMapper.readTree(raw)
            val response = tree.get("Response").asIterable()

            val json = when {
                kType.classifier == List::class -> response
                    .filterIsInstance<ObjectNode>()
                    .fold(objectMapper.createArrayNode()) { acc, jsonNode ->
                        acc.addAll(jsonNode.propertyNames().asSequence().map { jsonNode.get(it) }.toList())
                    }

                else -> {
                    response
                        .filterIsInstance<ObjectNode>()
                        .fold(objectMapper.createObjectNode()) { acc, jsonNode ->
                            acc.apply { setAll(jsonNode.properties().associate { it.key to it.value }) }
                        }
                }
            }

            return objectMapper
                .constructType(kType.javaType)
                .let { objectMapper.treeToValue(json, it) }
        }
    }

private val httpClient: java.net.http.HttpClient = java.net.http.HttpClient.newBuilder().build()

fun send(config: Config, req: Wirespec.RawRequest): Wirespec.RawResponse {
    val baseUri = java.net.URI(config.bunqServer.baseUrl + req.path.joinToString("/"))
    val uri = if (req.queries.isNotEmpty()) {
        val queryString = req.queries.entries.joinToString("&") { (key, value) ->
            value.joinToString("&") { v -> "$key=${java.net.URLEncoder.encode(v, Charsets.UTF_8)}" }
        }
        java.net.URI("$baseUri?$queryString")
    } else {
        baseUri
    }

    val headers = (req.headers + ("User-Agent" to listOf(config.userAgent?.takeIf { it.isNotBlank() } ?: config.serviceName)))
        .mapValues { (_, values) -> values.filter { it.isNotBlank() } }
        .flatMap { (key, values) -> values.map { key to it } }
        .flatMap { listOf(it.first, it.second) }.toTypedArray()
        .let {
            // Sign request
            if (req.body != null) {
                it + arrayOf("X-Bunq-Client-Signature", Signing.signData(config, String(req.body!!, Charsets.UTF_8)))
            } else {
                it
            }
        }

    val requestBuilder = java.net.http.HttpRequest.newBuilder()
        .uri(uri)
        .method(
            req.method.uppercase(), req.body
                ?.let { java.net.http.HttpRequest.BodyPublishers.ofByteArray(it) }
                ?: java.net.http.HttpRequest.BodyPublishers.noBody())
        .headers(*headers)

    // Send HTTP request
    logger.debug { "${req.method} $uri" }
    val response = httpClient.send(requestBuilder.build(), java.net.http.HttpResponse.BodyHandlers.ofByteArray())
    logger.debug { "${response.statusCode()} ${req.method} $uri" }

    // Construct Wirespec.RawResponse
    return Wirespec.RawResponse(
        statusCode = response.statusCode(),
        headers = response.headers().map(),
        body = response.body()
    )
}

fun Context.toHeaders(): Map<String, List<String>> = listOfNotNull(
    "X-Bunq-Client-Authentication" to sessionToken,
    config.cacheControl?.let { "Cache-Control" to it },
    config.language?.let { "X-Bunq-Language" to it },
    config.region?.let { "X-Bunq-Region" to it },
    config.clientRequestId?.let { "X-Bunq-Client-Request-Id" to it },
    config.geolocation?.let { "X-Bunq-GeoLocation" to it },
)
    .toMap()
    .mapValues { (_, value) -> listOf(value) }

fun bunqClient(context: Context): Client = Client(serialization, transportation(context))

fun bunqClient(config: Config): Client = bunqClient(initContext(config))

/**
 * Sends requests with the context's authentication headers.
 * When bunq answers 401 the session is refreshed once and the request is retried with the new session token.
 * The refreshed context is kept inside this transportation, so later requests use the new token.
 */
fun transportation(context: Context): Wirespec.Transportation {
    val current = AtomicReference(context)

    fun sendWith(used: Context, request: Wirespec.RawRequest) =
        send(used.config, request.copy(headers = request.headers + used.toHeaders()))

    return Wirespec.Transportation { request ->
        val used = current.get()
        val response = sendWith(used, request)
        if (response.statusCode != 401) return@Transportation response

        val refreshed = synchronized(current) {
            current.get().takeIf { it.sessionToken != used.sessionToken }
                ?: used.refreshSession().also(current::set)
        }
        sendWith(refreshed, request)
    }
}
