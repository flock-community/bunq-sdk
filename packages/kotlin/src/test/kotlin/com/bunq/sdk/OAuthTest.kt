package com.bunq.sdk

import com.sun.net.httpserver.HttpServer
import java.net.InetSocketAddress
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith

class OAuthTest {

    @Test
    fun `authorizeUrl encodes the parameters and includes state`() {
        val url = authorizeUrl(BUNQ_SANDBOX_OAUTH, "id 1", "https://app.example/cb?x=1&y=2", "s&t")

        assertEquals(
            "https://oauth.sandbox.bunq.com/auth?response_type=code&client_id=id+1" +
                "&redirect_uri=https%3A%2F%2Fapp.example%2Fcb%3Fx%3D1%26y%3D2&state=s%26t",
            url
        )
    }

    @Test
    fun `the public and sandbox servers use the documented URLs`() {
        assertEquals("https://oauth.bunq.com/auth", BUNQ_PUBLIC_OAUTH.authorizeUrl)
        assertEquals("https://api.oauth.bunq.com/v1/token", BUNQ_PUBLIC_OAUTH.tokenUrl)
        assertEquals("https://api-oauth.sandbox.bunq.com/v1/token", BUNQ_SANDBOX_OAUTH.tokenUrl)
    }

    private fun <T> answering(status: Int, body: String, seen: MutableList<String> = mutableListOf(), block: (OAuthServer) -> T): T {
        val server = HttpServer.create(InetSocketAddress("127.0.0.1", 0), 0)
        server.createContext("/") { exchange ->
            seen += "${exchange.requestMethod} ${exchange.requestURI} body=${exchange.requestBody.readAllBytes().size}"
            val bytes = body.toByteArray()
            exchange.sendResponseHeaders(status, bytes.size.toLong())
            exchange.responseBody.write(bytes)
            exchange.close()
        }
        server.start()
        try {
            return block(OAuthServer("", "http://127.0.0.1:${server.address.port}/v1/token"))
        } finally {
            server.stop(0)
        }
    }

    @Test
    fun `exchangeCode posts the parameters in the URL and returns the access token`() {
        val seen = mutableListOf<String>()
        val token = answering(200, """{"access_token":"tok","token_type":"bearer","state":"s"}""", seen) {
            exchangeCode(it, "id", "secret", "https://app.example/cb", "the code")
        }

        assertEquals("tok", token)
        assertEquals(
            listOf(
                "POST /v1/token?grant_type=authorization_code&code=the+code&redirect_uri=https%3A%2F%2Fapp.example%2Fcb" +
                    "&client_id=id&client_secret=secret body=0"
            ),
            seen
        )
    }

    @Test
    fun `exchangeCode throws with status and body on an error`() {
        val body = """{"error":"invalid_grant","error_description":"The authorization code is invalid or expired."}"""

        val e = assertFailsWith<BunqApiException> { answering(400, body) { exchangeCode(it, "id", "secret", "r", "c") } }

        assertEquals(400, e.status)
        assertEquals(body, e.body)
    }

    @Test
    fun `exchangeCode throws when a 200 has no access_token`() {
        val e = assertFailsWith<BunqApiException> { answering(200, "{}") { exchangeCode(it, "id", "secret", "r", "c") } }

        assertEquals(200, e.status)
    }
}
