package com.bunq.sdk

import com.bunq.sdk.generated.Client
import com.bunq.sdk.generated.endpoint.ReadUser
import com.sun.net.httpserver.HttpServer
import community.flock.wirespec.kotlin.Wirespec
import kotlinx.coroutines.runBlocking
import java.net.InetSocketAddress
import java.time.Instant
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertFailsWith
import kotlin.test.assertIs
import kotlin.test.assertTrue

class ErrorResponseTest {

    private fun readUser(status: Int, body: String) =
        ReadUser.fromRawResponse(serialization, Wirespec.RawResponse(status, emptyMap(), body.toByteArray()))

    private fun <T> answering(status: Int, body: String, headers: Map<String, String> = emptyMap(), block: (Client) -> T): T {
        val server = HttpServer.create(InetSocketAddress("127.0.0.1", 0), 0)
        server.createContext("/") { exchange ->
            headers.forEach { (name, value) -> exchange.responseHeaders.add(name, value) }
            TestServerKey.respond(exchange, status, body)
        }
        server.start()
        try {
            val config = Config(
                bunqServer = BunqServer("http://127.0.0.1:${server.address.port}/", ""),
                serviceName = "test",
                apiKey = "key",
                signingKeys = BunqSigningKeysGenerator.generateBunqSigningKeys(),
            )
            return block(bunqClient(Context(TestServerKey.publicPem, 1, 1, "token", 1, Instant.now().plusSeconds(3600), "installation", config)))
        } finally {
            server.stop(0)
        }
    }

    @Test
    fun `a 400 error body without Response envelope is a typed Response400`() {
        val body = """{"Error":[{"error_description":"Missing required field \"currency\"."}]}"""

        val response = answering(400, body) { runBlocking { it.readUser(1) } }

        assertIs<ReadUser.Response400>(response)
        assertEquals("Missing required field \"currency\".", response.body.Error?.single()?.error_description)
    }

    @Test
    fun `a body without Response or Error is rejected`() {
        assertFailsWith<IllegalStateException> { readUser(200, """{"unexpected":true}""") }
    }

    @Test
    fun `a status other than 200 and 400 throws with the status and body`() {
        for (status in listOf(403, 404, 500)) {
            val body = """{"Error":[{"error_description":"nope $status"}]}"""

            val e = assertFailsWith<BunqApiException> { answering(status, body) { runBlocking { it.readUser(1) } } }

            assertEquals(status, e.status)
            assertEquals(body, e.body)
        }
    }

    @Test
    fun `an HTML 500 throws with the HTML as body`() {
        val e = assertFailsWith<BunqApiException> { answering(500, "<html>Internal Server Error</html>") { runBlocking { it.readUser(1) } } }

        assertEquals(500, e.status)
        assertEquals("<html>Internal Server Error</html>", e.body)
    }

    @Test
    fun `a 400 that is not JSON throws`() {
        val e = assertFailsWith<BunqApiException> { answering(400, "<html>Bad Request</html>") { runBlocking { it.readUser(1) } } }

        assertEquals(400, e.status)
    }

    @Test
    fun `a 200 without Response throws with the status and body`() {
        val body = """{"unexpected":true}"""

        val e = assertFailsWith<BunqApiException> { answering(200, body) { runBlocking { it.readUser(1) } } }

        assertEquals(200, e.status)
        assertEquals(body, e.body)
    }

    @Test
    fun `a 400 without Error throws with the status and body`() {
        val body = """{"message":"Bad Request"}"""

        val e = assertFailsWith<BunqApiException> { answering(400, body) { runBlocking { it.readUser(1) } } }

        assertEquals(400, e.status)
        assertEquals(body, e.body)
    }

    @Test
    fun `a non-object JSON 200 throws`() {
        val e = assertFailsWith<BunqApiException> { answering(200, "[]") { runBlocking { it.readUser(1) } } }

        assertEquals(200, e.status)
        assertEquals("[]", e.body)
    }

    @Test
    fun `the exception carries the response headers but the message does not`() {
        val headers = mapOf("X-Bunq-Client-Response-Id" to "response-id-123", "Retry-After" to "30")

        val e = assertFailsWith<BunqApiException> {
            answering(429, """{"Error":[{"error_description":"Too many requests."}]}""", headers) { runBlocking { it.readUser(1) } }
        }

        assertEquals(listOf("response-id-123"), e.headers.entries.single { it.key.equals("X-Bunq-Client-Response-Id", ignoreCase = true) }.value)
        assertEquals(listOf("30"), e.headers.entries.single { it.key.equals("Retry-After", ignoreCase = true) }.value)
        assertFalse(e.message!!.contains("response-id-123"))
    }

    @Test
    fun `the message truncates the body but the body field keeps it whole`() {
        val e = BunqApiException(502, "x".repeat(2000))

        assertTrue(e.message!!.length < 600)
        assertEquals(2000, e.body.length)
    }

    @Test
    fun `a 200 is returned as is`() {
        val response = answering(200, """{"Response":[{"UserPerson":{"id":1}}]}""") { runBlocking { it.readUser(1) } }

        assertIs<ReadUser.Response200>(response)
    }
}
