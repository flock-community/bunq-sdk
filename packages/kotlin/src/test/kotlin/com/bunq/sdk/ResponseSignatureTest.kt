package com.bunq.sdk

import com.sun.net.httpserver.HttpServer
import community.flock.wirespec.kotlin.Wirespec
import kotlinx.coroutines.runBlocking
import java.net.InetSocketAddress
import java.time.Instant
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith
import kotlin.test.assertFalse
import kotlin.test.assertTrue

class ResponseSignatureTest {

    private val body = """{"Response":[]}"""
    private val request = Wirespec.RawRequest("GET", listOf("ping"), emptyMap(), emptyMap(), null)

    private fun call(status: Int = 200, signature: String?, responseBody: String = body): Wirespec.RawResponse {
        val server = HttpServer.create(InetSocketAddress("127.0.0.1", 0), 0)
        server.createContext("/") { TestServerKey.respond(it, status, responseBody, signature) }
        server.start()
        try {
            val config = Config(
                bunqServer = BunqServer("http://127.0.0.1:${server.address.port}/", ""),
                serviceName = "test",
                apiKey = "key",
                signingKeys = BunqSigningKeysGenerator.generateBunqSigningKeys(),
            )
            val context = Context(TestServerKey.publicPem, 1, 1, "token", 1, Instant.now().plusSeconds(3600), "installation", config)
            return runBlocking { transportation(context).transport(request) }
        } finally {
            server.stop(0)
        }
    }

    @Test
    fun `a valid signature passes`() {
        assertEquals(200, call(signature = TestServerKey.sign(body.toByteArray())).statusCode)
    }

    @Test
    fun `a valid signature on a 400 passes`() {
        val error = """{"Error":[{"error_description":"x"}]}"""
        assertEquals(400, call(400, TestServerKey.sign(error.toByteArray()), error).statusCode)
    }

    @Test
    fun `a 400 with an invalid signature throws`() {
        val e = assertFailsWith<SecurityException> { call(400, TestServerKey.sign("other".toByteArray()), """{"Error":[{"error_description":"x"}]}""") }
        assertEquals("Invalid bunq server signature", e.message)
    }

    @Test
    fun `a 400 with a missing signature throws`() {
        assertFailsWith<SecurityException> { call(400, null, """{"Error":[{"error_description":"x"}]}""") }
    }

    @Test
    fun `initContext throws on an unsigned device server response`() {
        val installation = """{"Response":[{"Id":{"id":1}},{"Token":{"token":"t"}},{"ServerPublicKey":{"server_public_key":${jsonString(TestServerKey.publicPem)}}}]}"""
        val server = HttpServer.create(InetSocketAddress("127.0.0.1", 0), 0)
        server.createContext("/") {
            TestServerKey.respond(it, 200, if (it.requestURI.path.endsWith("installation")) installation else """{"Response":[{"Id":{"id":3}}]}""", null)
        }
        server.start()
        try {
            val config = Config(
                bunqServer = BunqServer("http://127.0.0.1:${server.address.port}/", ""),
                serviceName = "test",
                apiKey = "key",
                signingKeys = BunqSigningKeysGenerator.generateBunqSigningKeys(),
            )
            val e = assertFailsWith<SecurityException> { initContext(config) }
            assertEquals("Invalid bunq server signature", e.message)
        } finally {
            server.stop(0)
        }
    }

    private fun jsonString(s: String) = "\"" + s.replace("\n", "\\n") + "\""

    @Test
    fun `a signature over another body throws`() {
        val e = assertFailsWith<SecurityException> { call(signature = TestServerKey.sign("other".toByteArray())) }
        assertEquals("Invalid bunq server signature", e.message)
    }

    @Test
    fun `a missing signature throws`() {
        assertFailsWith<SecurityException> { call(signature = null) }
    }

    @Test
    fun `a signature that is not base64 throws`() {
        assertFailsWith<SecurityException> { call(signature = "not base64!") }
    }

    @Test
    fun `verifyResponse checks the raw body bytes`() {
        val bytes = "{\"a\": 1}\n".toByteArray()
        val signature = TestServerKey.sign(bytes)
        assertTrue(Signing.verifyResponse(TestServerKey.publicPem, bytes, signature))
        assertFalse(Signing.verifyResponse(TestServerKey.publicPem, """{"a":1}""".toByteArray(), signature))
        assertFalse(Signing.verifyResponse(TestServerKey.publicPem, bytes, null))
    }
}
