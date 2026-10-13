package com.bunq.sdk

import com.sun.net.httpserver.HttpServer
import community.flock.wirespec.kotlin.Wirespec
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.async
import kotlinx.coroutines.awaitAll
import kotlinx.coroutines.runBlocking
import java.net.InetSocketAddress
import java.time.Instant
import java.util.concurrent.atomic.AtomicInteger
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith

class TransportationRefreshTest {

    private val authenticationError = """{"Error":[{"error_description":"Insufficient authentication."}]}"""
    private val request = Wirespec.RawRequest("GET", listOf("ping"), emptyMap(), emptyMap(), null)

    /** Answers 200 for the token "fresh", otherwise 403 with [rejection]. Returns the tokens it saw. */
    private fun withServer(rejection: String, block: (Context, List<String>) -> Unit) {
        val seenTokens = java.util.Collections.synchronizedList(mutableListOf<String>())
        val server = HttpServer.create(InetSocketAddress("127.0.0.1", 0), 0)
        server.createContext("/") { exchange ->
            val token = exchange.requestHeaders.getFirst("X-Bunq-Client-Authentication")
            seenTokens += token
            val (status, body) = if (token == "fresh") 200 to """{"Response":[]}""" else 403 to rejection
            val bytes = body.toByteArray()
            exchange.sendResponseHeaders(status, if (bytes.isEmpty()) -1 else bytes.size.toLong())
            if (bytes.isNotEmpty()) exchange.responseBody.write(bytes)
            exchange.close()
        }
        server.start()
        try {
            val config = Config(
                bunqServer = BunqServer("http://127.0.0.1:${server.address.port}/", ""),
                serviceName = "test",
                apiKey = "key",
                signingKeys = BunqSigningKeysGenerator.generateBunqSigningKeys(),
            )
            val context = Context("", 1, 1, "stale", 1, Instant.now(), "installation", config)
            block(context, seenTokens)
        } finally {
            server.stop(0)
        }
    }

    private fun Context.fresh() = copy(sessionToken = "fresh")

    @Test
    fun `insufficient authentication refreshes once and retries with the new token`() = withServer(authenticationError) { context, tokens ->
        val refreshes = AtomicInteger()
        val transport = transportation(context) { refreshes.incrementAndGet(); it.fresh() }

        val response = runBlocking { transport.transport(request) }

        assertEquals(200, response.statusCode)
        assertEquals(1, refreshes.get())
        assertEquals(listOf("stale", "fresh"), tokens)
    }

    @Test
    fun `a failing refresh throws the original 403`() = withServer(authenticationError) { context, tokens ->
        val transport = transportation(context) { error("429") }

        val e = assertFailsWith<BunqApiException> { runBlocking { transport.transport(request) } }

        assertEquals(403, e.status)
        assertEquals(authenticationError, e.body)
        assertEquals(listOf("stale"), tokens)
    }

    @Test
    fun `another 403 does not refresh`() = withServer("""{"Error":[{"error_description":"You are not allowed to make this call."}]}""") { context, _ ->
        val refreshes = AtomicInteger()
        val transport = transportation(context) { refreshes.incrementAndGet(); it.fresh() }

        assertEquals(403, assertFailsWith<BunqApiException> { runBlocking { transport.transport(request) } }.status)
        assertEquals(0, refreshes.get())
    }

    @Test
    fun `a 403 with an empty body does not refresh`() = withServer("") { context, _ ->
        val refreshes = AtomicInteger()
        val transport = transportation(context) { refreshes.incrementAndGet(); it.fresh() }

        assertEquals(403, assertFailsWith<BunqApiException> { runBlocking { transport.transport(request) } }.status)
        assertEquals(0, refreshes.get())
    }

    @Test
    fun `a 403 with an HTML body throws and does not refresh`() = withServer("<html>forbidden</html>") { context, _ ->
        val refreshes = AtomicInteger()
        val transport = transportation(context) { refreshes.incrementAndGet(); it.fresh() }

        val e = assertFailsWith<BunqApiException> { runBlocking { transport.transport(request) } }

        assertEquals(403, e.status)
        assertEquals("<html>forbidden</html>", e.body)
        assertEquals(0, refreshes.get())
    }

    @Test
    fun `concurrent calls refresh once`() = withServer(authenticationError) { context, _ ->
        val refreshes = AtomicInteger()
        val transport = transportation(context) { Thread.sleep(200); refreshes.incrementAndGet(); it.fresh() }

        val statuses = runBlocking {
            (1..2).map { async(Dispatchers.Default) { transport.transport(request).statusCode } }.awaitAll()
        }

        assertEquals(listOf(200, 200), statuses)
        assertEquals(1, refreshes.get())
    }
}
