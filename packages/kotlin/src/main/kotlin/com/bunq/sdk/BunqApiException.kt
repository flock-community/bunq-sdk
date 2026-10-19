package com.bunq.sdk

/** bunq (or a proxy in front of it) answered with a status other than 200 or 400, or with a 400 that is not JSON. */
class BunqApiException(val status: Int, val body: String) :
    RuntimeException("Received $status: ${body.take(MAX_MESSAGE_BODY)}") {
    private companion object {
        const val MAX_MESSAGE_BODY = 500
    }
}
