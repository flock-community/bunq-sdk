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
import kotlin.test.assertFailsWith
import kotlin.test.assertIs
import kotlin.test.assertTrue

class ErrorResponseTest {

    private fun readUser(status: Int, body: String) =
        ReadUser.fromRawResponse(serialization, Wirespec.RawResponse(status, emptyMap(), body.toByteArray()))

    private fun <T> answering(status: Int, body: String, block: (Client) -> T): T {
        val server = HttpServer.create(InetSocketAddress("127.0.0.1", 0), 0)
        server.createContext("/") { exchange ->
            val bytes = body.toByteArray()
            exchange.sendResponseHeaders(status, bytes.size.toLong())
            exchange.responseBody.write(bytes)
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
            return block(bunqClient(Context("", 1, 1, "token", 1, Instant.now(), "installation", config)))
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
