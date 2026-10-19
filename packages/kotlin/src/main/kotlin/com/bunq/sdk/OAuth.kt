package com.bunq.sdk

import java.net.URI
import java.net.URLEncoder
import java.net.http.HttpRequest
import java.net.http.HttpResponse
import tools.jackson.core.JacksonException

/** The two bunq OAuth endpoints: where the user is sent to authorize, and where the code is exchanged for a token. */
data class OAuthServer(
    val authorizeUrl: String,
    val tokenUrl: String,
)

val BUNQ_PUBLIC_OAUTH = OAuthServer(
    "https://oauth.bunq.com/auth",
    "https://api.oauth.bunq.com/v1/token",
)

val BUNQ_SANDBOX_OAUTH = OAuthServer(
    "https://oauth.sandbox.bunq.com/auth",
    "https://api-oauth.sandbox.bunq.com/v1/token",
)

private fun query(params: List<Pair<String, String>>) =
    params.joinToString("&") { (k, v) -> "$k=${URLEncoder.encode(v, Charsets.UTF_8)}" }

/** The URL to send the user to. bunq redirects back to [redirectUri] with `code` and the same [state]; check the state on return. */
fun authorizeUrl(server: OAuthServer, clientId: String, redirectUri: String, state: String): String =
    server.authorizeUrl + "?" + query(
        listOf("response_type" to "code", "client_id" to clientId, "redirect_uri" to redirectUri, "state" to state)
    )

/**
 * Exchanges the authorization [code] for an access token, which can be used as `Config.apiKey`.
 * [redirectUri] must be the one used in [authorizeUrl]. Any status other than 200, and a 200 without a string `access_token`, throws [BunqApiException].
 */
fun exchangeCode(server: OAuthServer, clientId: String, clientSecret: String, redirectUri: String, code: String): String {
    val params = query(
        listOf(
            "grant_type" to "authorization_code", "code" to code, "redirect_uri" to redirectUri,
            "client_id" to clientId, "client_secret" to clientSecret,
        )
    )
    // bunq expects the parameters in the URL and no body
    val request = HttpRequest.newBuilder(URI("${server.tokenUrl}?$params"))
        .POST(HttpRequest.BodyPublishers.noBody())
        .build()
    val response = httpClient.send(request, HttpResponse.BodyHandlers.ofString())
    if (response.statusCode() != 200) throw BunqApiException(response.statusCode(), response.body())
    val tree = try {
        objectMapper.readTree(response.body())
    } catch (e: JacksonException) {
        throw BunqApiException(200, response.body())
    }
    return tree.get("access_token")?.takeIf { it.isString }?.asString()
        ?: throw BunqApiException(200, response.body())
}
