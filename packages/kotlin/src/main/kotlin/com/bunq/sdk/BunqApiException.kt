package com.bunq.sdk

/**
 * bunq (or a proxy in front of it) answered with a status other than 200 or 400, or with a 400 that is not JSON.
 * [headers] are the response headers (for example `X-Bunq-Client-Response-Id`); they are left out of the message, which ends up in logs.
 */
class BunqApiException @JvmOverloads constructor(
    val status: Int,
    val body: String,
    val headers: Map<String, List<String>> = emptyMap(),
) : RuntimeException("Received $status: ${body.take(MAX_MESSAGE_BODY)}") {
    private companion object {
        const val MAX_MESSAGE_BODY = 500
    }
}
