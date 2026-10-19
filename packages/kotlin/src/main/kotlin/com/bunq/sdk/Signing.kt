package com.bunq.sdk

import io.github.oshai.kotlinlogging.KotlinLogging
import org.bouncycastle.jce.provider.BouncyCastleProvider
import java.nio.charset.StandardCharsets
import java.security.Security
import java.security.Signature
import java.util.Base64


object Signing{
    private val logger = KotlinLogging.logger {}
    init {
        if (Security.getProvider("BC") == null) {
            Security.addProvider(BouncyCastleProvider())
        }
    }

    fun signData(config: Config, data: String): String {
        val privateKey = config.signingKeys.privateKey()
        // Ensure the data is encoded in UTF-8 exactly as it will be sent
        val encodedData = data.toByteArray(StandardCharsets.UTF_8)

        // Generate signature using SHA256 and PKCS#1 v1.5 padding
        val signature = Signature.getInstance("SHA256withRSA")
            .apply {
                initSign(privateKey)
                update(encodedData)
            }
            .sign()

        // Encode in Base64
        return Base64.getEncoder().encodeToString(signature)
    }

    /** Verifies bunq's `X-Bunq-Server-Signature`: SHA256withRSA over the raw response body bytes. */
    fun verifyResponse(
        serverPublicKeyPem: String,
        responseBody: ByteArray,
        signature: String?,
    ): Boolean = try {
        val decodedSignature = Base64.getDecoder().decode(signature ?: return false)

        val verifier = Signature.getInstance("SHA256withRSA", "BC")
        verifier.initVerify(validateAndLoadPublicKey(serverPublicKeyPem))
        verifier.update(responseBody)

        verifier.verify(decodedSignature)
    } catch (e: Exception) {
        logger.error(e) { "Signature verification failed" }
        false
    }
}
