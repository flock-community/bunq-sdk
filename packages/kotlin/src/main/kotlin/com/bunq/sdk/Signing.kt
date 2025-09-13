package com.bunq.sdk

import org.bouncycastle.jce.provider.BouncyCastleProvider
import java.nio.charset.StandardCharsets
import java.security.Security
import java.security.Signature
import java.util.Base64


object Signing{
    init {
        if (Security.getProvider("BC") == null) {
            Security.addProvider(BouncyCastleProvider())
        }
    }

    fun signData(config: Config, data: String): String {
        val privateKey = config.privateKey
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

    fun verifyResponse(
        config: Config,
        responseBody: String,
        signature: String,
    ): Boolean = try {
        val publicKey = config.publicKey
        val decodedSignature = Base64.getDecoder().decode(signature)

        val verifier = Signature.getInstance("SHA256withRSA", "BC")
        verifier.initVerify(publicKey)
        verifier.update(responseBody.toByteArray(Charsets.UTF_8))

        verifier.verify(decodedSignature)
    } catch (e: Exception) {
        println("[ERROR] Signature verification failed: ${e.message}")
        false
    }
}


