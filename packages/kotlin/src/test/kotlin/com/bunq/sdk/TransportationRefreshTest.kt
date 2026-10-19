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

    /** Set by [fresh]: like bunq, the server accepts the session again after a refresh although the token stays the same. */
    private val revived = java.util.concurrent.atomic.AtomicBoolean()

    /** Answers 200 once [revived], otherwise 403 with [rejection]. Returns the tokens it saw. */
    private fun withServer(rejection: String, expiry: Instant = Instant.now().plusSeconds(3600), block: (Context, List<String>) -> Unit) {
        val seenTokens = java.util.Collections.synchronizedList(mutableListOf<String>())
        val server = HttpServer.create(InetSocketAddress("127.0.0.1", 0), 0)
        server.createContext("/") { exchange ->
            val token = exchange.requestHeaders.getFirst("X-Bunq-Client-Authentication")
            seenTokens += token
            val (status, body) = if (revived.get()) 200 to """{"Response":[]}""" else 403 to rejection
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
            val context = Context("", 1, 1, "stale", 1, expiry, "installation", config)
            block(context, seenTokens)
        } finally {
            server.stop(0)
        }
    }

    /** What bunq returns for a re-created session: the same token with a later expiry. */
    private fun Context.fresh(): Context {
        revived.set(true)
        return copy(sessionExpiryTime = Instant.now().plusSeconds(3600))
    }

    @Test
    fun `insufficient authentication refreshes once and retries with the new token`() = withServer(authenticationError) { context, tokens ->
        val refreshes = AtomicInteger()
        val transport = refreshingTransportation(context) { refreshes.incrementAndGet(); it.fresh() }

        val response = runBlocking { transport.transport(request) }

        assertEquals(200, response.statusCode)
        assertEquals(1, refreshes.get())
        assertEquals(listOf("stale", "stale"), tokens)
    }

    @Test
    fun `a failing refresh throws the original 403`() = withServer(authenticationError) { context, tokens ->
        val transport = refreshingTransportation(context) { error("429") }

        val e = assertFailsWith<BunqApiException> { runBlocking { transport.transport(request) } }

        assertEquals(403, e.status)
        assertEquals(authenticationError, e.body)
        assertEquals(listOf("stale"), tokens)
    }

    @Test
    fun `another 403 does not refresh`() = withServer("""{"Error":[{"error_description":"You are not allowed to make this call."}]}""") { context, _ ->
        val refreshes = AtomicInteger()
        val transport = refreshingTransportation(context) { refreshes.incrementAndGet(); it.fresh() }

        assertEquals(403, assertFailsWith<BunqApiException> { runBlocking { transport.transport(request) } }.status)
        assertEquals(0, refreshes.get())
    }

    @Test
    fun `a 403 with an empty body does not refresh`() = withServer("") { context, _ ->
        val refreshes = AtomicInteger()
        val transport = refreshingTransportation(context) { refreshes.incrementAndGet(); it.fresh() }

        assertEquals(403, assertFailsWith<BunqApiException> { runBlocking { transport.transport(request) } }.status)
        assertEquals(0, refreshes.get())
    }

    @Test
    fun `a 403 with an HTML body throws and does not refresh`() = withServer("<html>forbidden</html>") { context, _ ->
        val refreshes = AtomicInteger()
        val transport = refreshingTransportation(context) { refreshes.incrementAndGet(); it.fresh() }

        val e = assertFailsWith<BunqApiException> { runBlocking { transport.transport(request) } }

        assertEquals(403, e.status)
        assertEquals("<html>forbidden</html>", e.body)
        assertEquals(0, refreshes.get())
    }

    @Test
    fun `concurrent calls refresh once`() = withServer(authenticationError) { context, _ ->
        val refreshes = AtomicInteger()
        val transport = refreshingTransportation(context) { Thread.sleep(200); refreshes.incrementAndGet(); it.fresh() }

        val statuses = runBlocking {
            (1..2).map { async(Dispatchers.Default) { transport.transport(request).statusCode } }.awaitAll()
        }

        assertEquals(listOf(200, 200), statuses)
        assertEquals(1, refreshes.get())
    }

    @Test
    fun `an expired context is refreshed before the first request and the callback fires once`() =
        withServer(authenticationError, expiry = Instant.now().minusSeconds(1)) { context, tokens ->
            val refreshes = AtomicInteger()
            val changes = java.util.Collections.synchronizedList(mutableListOf<Context>())
            val transport = refreshingTransportation(context, { changes += it }) { refreshes.incrementAndGet(); it.fresh() }

            assertEquals(200, runBlocking { transport.transport(request) }.statusCode)

            assertEquals(1, refreshes.get())
            assertEquals(listOf("stale"), tokens)
            assertEquals(1, changes.size)
        }

    @Test
    fun `a context that is not expired is not refreshed`() = withServer(authenticationError) { context, tokens ->
        val refreshes = AtomicInteger()
        revived.set(true)
        val transport = refreshingTransportation(context, { refreshes.incrementAndGet() }) { refreshes.incrementAndGet(); it }

        assertEquals(200, runBlocking { transport.transport(request) }.statusCode)

        assertEquals(0, refreshes.get())
        assertEquals(listOf("stale"), tokens)
    }

    @Test
    fun `a 403 refresh calls the callback once with the new context`() = withServer(authenticationError) { context, _ ->
        val changes = java.util.Collections.synchronizedList(mutableListOf<Context>())
        val transport = refreshingTransportation(context, { changes += it }) { it.fresh() }

        assertEquals(200, runBlocking { transport.transport(request) }.statusCode)

        assertEquals(1, changes.size)
    }

    @Test
    fun `concurrent calls on an expired context refresh once when bunq keeps the session token`() =
        withServer(authenticationError, expiry = Instant.now().minusSeconds(1)) { context, _ ->
            val refreshes = AtomicInteger()
            val changes = AtomicInteger()
            val transport = refreshingTransportation(context, { changes.incrementAndGet() }) { Thread.sleep(200); refreshes.incrementAndGet(); it.fresh() }

            val statuses = runBlocking {
                (1..3).map { async(Dispatchers.Default) { transport.transport(request).statusCode } }.awaitAll()
            }

            assertEquals(listOf(200, 200, 200), statuses)
            assertEquals(1, refreshes.get())
            assertEquals(1, changes.get())
        }

    @Test
    fun `a failed refresh before sending is not repeated after the 403`() =
        withServer(authenticationError, expiry = Instant.now().minusSeconds(1)) { context, _ ->
            val refreshes = AtomicInteger()
            val transport = refreshingTransportation(context) { refreshes.incrementAndGet(); error("429") }

            assertEquals(403, assertFailsWith<BunqApiException> { runBlocking { transport.transport(request) } }.status)
            assertEquals(1, refreshes.get())
        }

    @Test
    fun `a context expiring in 10 seconds is refreshed`() =
        withServer(authenticationError, expiry = Instant.now().plusSeconds(10)) { context, tokens ->
            val refreshes = AtomicInteger()
            val transport = refreshingTransportation(context) { refreshes.incrementAndGet(); it.fresh() }

            assertEquals(200, runBlocking { transport.transport(request) }.statusCode)
            assertEquals(1, refreshes.get())
            assertEquals(listOf("stale"), tokens) // refreshed before sending: no rejected request first
        }
}
