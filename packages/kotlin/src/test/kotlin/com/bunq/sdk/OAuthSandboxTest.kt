package com.bunq.sdk

import com.bunq.sdk.generated.endpoint.CreateCallbackUrlForUserOauthClient
import com.bunq.sdk.generated.endpoint.CreateOauthClientForUser
import com.bunq.sdk.generated.endpoint.ListAllOauthClientForUser
import com.bunq.sdk.generated.endpoint.ReadUser
import com.bunq.sdk.generated.model.OauthCallbackUrl
import com.bunq.sdk.generated.model.OauthClient
import com.sun.net.httpserver.HttpServer
import kotlinx.coroutines.test.runTest
import org.junit.jupiter.api.condition.EnabledIfEnvironmentVariable
import java.net.InetSocketAddress
import java.net.URI
import java.net.URLDecoder
import java.net.http.HttpClient
import java.net.http.HttpRequest
import java.net.http.HttpResponse
import java.util.UUID
import java.util.concurrent.CompletableFuture
import java.util.concurrent.TimeUnit
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertNotNull

/**
 * End-to-end OAuth flow against the bunq sandbox. The authorize page shows a QR code that the user scans with the bunq sandbox app,
 * so a human has to approve: run with `BUNQ_OAUTH_E2E=1` and watch the test output for the authorize URL.
 *
 * `BUNQ_OAUTH_E2E_API_KEY`: sandbox API key of a user you can log in with in the sandbox app (default: a new sandbox user, whose app login is unknown).
 * `BUNQ_OAUTH_E2E_TIMEOUT_SECONDS`: how long to wait for the approval (default 300).
 */
@EnabledIfEnvironmentVariable(named = "BUNQ_OAUTH_E2E", matches = "1")
class OAuthSandboxTest {

    private fun newSandboxApiKey(): String {
        val request = HttpRequest.newBuilder(URI.create(BUNQ_SANDBOX_SERVER.baseUrl + "sandbox-user-person"))
            .header("User-Agent", "OAuthSandboxTest")
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString("{}"))
            .build()
        val response = HttpClient.newHttpClient().send(request, HttpResponse.BodyHandlers.ofString())
        assertEquals(200, response.statusCode())
        return objectMapper.readTree(response.body())["Response"].firstNotNullOf { it["ApiKey"] }["api_key"].asString()
    }

    private fun config(apiKey: String) = Config(
        bunqServer = BUNQ_SANDBOX_SERVER,
        serviceName = "OAuthSandboxTest",
        apiKey = apiKey,
        signingKeys = BunqSigningKeysGenerator.generateBunqSigningKeys(),
    )

    @Test
    fun `authorize with the bunq sandbox app and use the access token`(): Unit = runTest {
        // 1 + 2: sandbox user and handshake
        val apiKey = System.getenv("BUNQ_OAUTH_E2E_API_KEY") ?: newSandboxApiKey()
        val context = initContext(config(apiKey))
        val client = bunqClient(context)
        println("sandbox user ${context.userId}")

        // 3: the OAuth client (one per user), and the redirect URL on it
        val existing = (client.listAllOauthClientForUser(context.userId, null, null, null) as ListAllOauthClientForUser.Response200).body.Response
        val oauthClient = existing.firstOrNull() ?: run {
            check(client.createOauthClientForUser(context.userId, OauthClient("ACTIVE")) is CreateOauthClientForUser.Response200)
            (client.listAllOauthClientForUser(context.userId, null, null, null) as ListAllOauthClientForUser.Response200).body.Response.first()
        }
        val clientId = assertNotNull(oauthClient.client_id)
        val clientSecret = assertNotNull(oauthClient.secret)

        // 4: local callback server on a free port
        val received = CompletableFuture<Map<String, String>>()
        val server = HttpServer.create(InetSocketAddress("127.0.0.1", 0), 0)
        server.createContext("/callback") { exchange ->
            val params = (exchange.requestURI.rawQuery ?: "").split("&").filter { it.isNotEmpty() }.associate {
                it.substringBefore("=") to URLDecoder.decode(it.substringAfter("=", ""), Charsets.UTF_8)
            }
            val page = "You can close this tab.".toByteArray()
            exchange.sendResponseHeaders(200, page.size.toLong())
            exchange.responseBody.use { it.write(page) }
            received.complete(params)
        }
        server.start()
        try {
            val redirectUri = "http://127.0.0.1:${server.address.port}/callback"
            val added = client.createCallbackUrlForUserOauthClient(context.userId, oauthClient.id!!, OauthCallbackUrl(redirectUri))
            check(added is CreateCallbackUrlForUserOauthClient.Response200) { "bunq rejected the redirect URL $redirectUri: $added" }

            // 5: the user approves on the authorize page by scanning its QR code with the sandbox app
            val state = UUID.randomUUID().toString()
            println("Open this URL in a browser and scan the QR code with the bunq sandbox app (logged in as sandbox user ${context.userId}):")
            println(authorizeUrl(BUNQ_SANDBOX_OAUTH, clientId, redirectUri, state))
            val timeout = System.getenv("BUNQ_OAUTH_E2E_TIMEOUT_SECONDS")?.toLong() ?: 300
            val params = received.get(timeout, TimeUnit.SECONDS)

            // 6: exchange the code
            assertEquals(state, params["state"], "state returned by bunq")
            val code = assertNotNull(params["code"], "code in the callback: $params")
            val accessToken = exchangeCode(BUNQ_SANDBOX_OAUTH, clientId, clientSecret, redirectUri, code)
            println("got an access token of ${accessToken.length} characters")

            // 7: use the token as the API key
            val oauthContext = initContext(config(accessToken))
            val res = bunqClient(oauthContext).readUser(oauthContext.userId)
            val body = (res as ReadUser.Response200).body
            println("readUser as OAuth user ${oauthContext.userId}: ${body.UserApiKey}")
            assertNotNull(body.UserApiKey, "an OAuth token opens a UserApiKey user")
        } finally {
            server.stop(0)
        }
    }
}
