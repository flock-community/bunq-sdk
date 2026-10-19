package com.bunq.sdk

import com.sun.net.httpserver.HttpExchange
import java.security.Signature
import java.util.Base64

/** Stands in for bunq's server key: local test servers sign their responses with it. */
internal object TestServerKey {
    private val keys = BunqSigningKeysGenerator.generateBunqSigningKeys()
    val publicPem: String = keys.publicKeyAsPem()

    fun sign(body: ByteArray): String = Base64.getEncoder().encodeToString(
        Signature.getInstance("SHA256withRSA").apply { initSign(keys.privateKey()); update(body) }.sign()
    )

    /** Answers with [body] and an X-Bunq-Server-Signature header (none when [signature] is null). */
    fun respond(exchange: HttpExchange, status: Int, body: String, signature: String? = sign(body.toByteArray())) {
        val bytes = body.toByteArray()
        signature?.let { exchange.responseHeaders.add("X-Bunq-Server-Signature", it) }
        exchange.sendResponseHeaders(status, if (bytes.isEmpty()) -1 else bytes.size.toLong())
        if (bytes.isNotEmpty()) exchange.responseBody.write(bytes)
        exchange.close()
    }
}
