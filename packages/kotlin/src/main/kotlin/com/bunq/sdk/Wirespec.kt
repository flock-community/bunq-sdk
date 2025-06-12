@file:OptIn(ExperimentalStdlibApi::class)

package com.bunq.sdk

import com.fasterxml.jackson.databind.DeserializationFeature
import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.databind.node.ObjectNode
import com.fasterxml.jackson.module.kotlin.KotlinFeature
import com.fasterxml.jackson.module.kotlin.kotlinModule
import community.flock.wirespec.integration.jackson.kotlin.WirespecModuleKotlin
import community.flock.wirespec.kotlin.Wirespec
import community.flock.wirespec.kotlin.Wirespec.ParamSerialization
import community.flock.wirespec.kotlin.serde.DefaultParamSerialization
import kotlin.reflect.KClass
import kotlin.reflect.KType
import kotlin.reflect.full.companionObjectInstance
import kotlin.reflect.full.memberProperties
import kotlin.reflect.javaType

val baseUrl = "https://public-api.sandbox.bunq.com/v1/"

val objectMapper: ObjectMapper = ObjectMapper()
    .configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false)
    .registerModule(kotlinModule {
        enable(KotlinFeature.KotlinPropertyNameAsImplicitName)
    })
    .registerModule(WirespecModuleKotlin())


val serialization: Wirespec.Serialization<String> =
    object : Wirespec.Serialization<String>, ParamSerialization by DefaultParamSerialization() {
        override fun <T> serialize(t: T, kType: KType): String {
            if (t is Unit) return ""
            return objectMapper.writeValueAsString(t)
        }

        override fun <T> deserialize(raw: String, kType: KType): T {
            val tree = objectMapper.readTree(raw)
            val response = tree.get("Response").asIterable()

            val json = when {
                kType.classifier == List::class -> response
                    .filterIsInstance<ObjectNode>()
                    .fold(objectMapper.createArrayNode()) { acc, jsonNode ->
                        acc.addAll(jsonNode.fieldNames().asSequence().map { jsonNode.get(it) }.toList())
                    }

                else -> {
                    response
                        .filterIsInstance<ObjectNode>()
                        .fold(objectMapper.createObjectNode()) { acc, jsonNode ->
                            acc.apply { setAll<ObjectNode>(jsonNode) }
                        }
                        .let { json ->
                            val fields = json.fieldNames().asSequence().toList()
                            val classifier = kType.classifier as KClass<*>
                            val members = classifier.memberProperties.map { it.name }
                            if (members.intersect(fields).isEmpty()) json.first() else json
                        }
                }
            }

            return objectMapper
                .constructType(kType.javaType)
                .let { objectMapper.treeToValue(json, it) }
        }
    }

fun send(signing: Signing, req: Wirespec.RawRequest): Wirespec.RawResponse {
    val client = java.net.http.HttpClient.newBuilder().build()

    val baseUri = java.net.URI(baseUrl + req.path.joinToString("/"))
    val uri = if (req.queries.isNotEmpty()) {
        val queryString = req.queries.entries.joinToString("&") { (key, value) ->
            value.joinToString("&") { v -> "$key=${java.net.URLEncoder.encode(v, Charsets.UTF_8)}" }
        }
        java.net.URI("$baseUri?$queryString")
    } else {
        baseUri
    }

    val headers = req.headers
        .mapValues { (_, values) -> values.filter { it.isNotBlank() } }
        .flatMap { (key, values) -> values.map { key to it } }
        .flatMap { listOf(it.first, it.second) }.toTypedArray()
        .let {
            // Sign request
            if (req.body != null) {
                it + arrayOf("X-Bunq-Client-Signature", signing.signData(req.body!!))
            } else {
                it
            }
        }

    val requestBuilder = java.net.http.HttpRequest.newBuilder()
        .uri(uri)
        .method(
            req.method.uppercase(), req.body
                ?.let { java.net.http.HttpRequest.BodyPublishers.ofString(it) }
                ?: java.net.http.HttpRequest.BodyPublishers.noBody())
        .headers(*headers)

    // Send HTTP request
    val response = client.send(requestBuilder.build(), java.net.http.HttpResponse.BodyHandlers.ofString())

    // Construct Wirespec.RawResponse
    return Wirespec.RawResponse(
        statusCode = response.statusCode(),
        headers = response.headers().map(),
        body = response.body()
    )
}

fun Context.toHeaders(): Map<String, List<String>> = listOfNotNull(
    "X-Bunq-Client-Authentication" to sessionToken,
    userAgent?.let { "UserAgent" to it },
    cacheControl?.let { "CacheControl" to it },
    language?.let { "X-Bunq-Language" to it },
    region?.let { "X-Bunq-Region" to it },
    clientRequestId?.let { "X-Bunq-Client-Request-Id" to it },
    geolocation?.let { "X-Bunq-GeoLocation" to it },
)
    .toMap()
    .mapValues { (_, value) -> listOf(value) }

fun <Req : Wirespec.Request<*>, Res : Wirespec.Response<*>> handle(
    signing: Signing,
    context: Context,
    request: Req
): Res {
    val declaringClass = request::class.java.declaringClass
    val handler =
        declaringClass.declaredClasses.toList().find { it.simpleName == "Handler" } ?: error("Handler not found")
    val instance = handler.kotlin.companionObjectInstance as Wirespec.Client<Wirespec.Request<*>, Wirespec.Response<*>>
    val client = instance.client(serialization)
    val rawRequest = client.to(request as Wirespec.Request<*>)
    val reqToken = rawRequest.copy(headers = rawRequest.headers + context.toHeaders())
    val rawResponse = send(signing, reqToken)
    return client.from(rawResponse) as Res
}

fun handler(signing: Signing, context: Context): (Wirespec.Request<*>) -> Wirespec.Response<*> =
    { req -> handle(signing, context, req) }

fun handler(config: Config): (Wirespec.Request<*>) -> Wirespec.Response<*> {
    val signing = Signing(config)
    val context = initContext(config)
    return { req -> handle(signing, context, req) }
}

