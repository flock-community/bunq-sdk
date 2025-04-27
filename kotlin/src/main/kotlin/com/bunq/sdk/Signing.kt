package com.bunq.sdk

import org.bouncycastle.jce.provider.BouncyCastleProvider
import org.bouncycastle.util.io.pem.PemObject
import org.bouncycastle.util.io.pem.PemReader
import org.bouncycastle.util.io.pem.PemWriter
import java.io.StringReader
import java.io.StringWriter
import java.nio.charset.StandardCharsets
import java.security.KeyFactory
import java.security.KeyPairGenerator
import java.security.PrivateKey
import java.security.PublicKey
import java.security.SecureRandom
import java.security.Security
import java.security.Signature
import java.security.spec.PKCS8EncodedKeySpec
import java.security.spec.X509EncodedKeySpec
import java.util.Base64

class Signing(private val config: Config) {
    init {
        if (Security.getProvider("BC") == null) {
            Security.addProvider(BouncyCastleProvider())
        }
    }

    fun generateRsaKeyPair(): Pair<String, String> {
        if (config.privateKeyFile.exists() && config.publicKeyFile.exists()) {
            val privateKeyPem = config.privateKeyFile.readText()
            val publicKeyPem = config.publicKeyFile.readText()
            return Pair(privateKeyPem, publicKeyPem)
        }

        val keyPairGenerator = KeyPairGenerator.getInstance("RSA", "BC")
        keyPairGenerator.initialize(2048, SecureRandom())
        val keyPair = keyPairGenerator.generateKeyPair()

        val privateKeyPem = convertPrivateKeyToPem(keyPair.private)
        val publicKeyPem = convertPublicKeyToPem(keyPair.public)

        config.privateKeyFile.writeText(privateKeyPem)
        config.publicKeyFile.writeText(publicKeyPem)

        println("bunq - creating new keypair [KEEP THESE FILES SAFE]")
        return Pair(privateKeyPem, publicKeyPem)
    }

    private fun convertPrivateKeyToPem(privateKey: PrivateKey): String {
        return StringWriter().use { stringWriter ->
            PemWriter(stringWriter).use { pemWriter ->
                pemWriter.writeObject(PemObject("PRIVATE KEY", privateKey.encoded))
            }
            stringWriter.toString()
        }
    }

    private fun convertPublicKeyToPem(publicKey: PublicKey): String {
        return StringWriter().use { stringWriter ->
            PemWriter(stringWriter).use { pemWriter ->
                pemWriter.writeObject(PemObject("PUBLIC KEY", publicKey.encoded))
            }
            stringWriter.toString()
        }
    }

    private fun loadPrivateKey(): PrivateKey {
        val privateKeyPem = config.privateKeyFile.readText()
        val keyFactory = KeyFactory.getInstance("RSA", "BC")
        val pemContent = PemReader(StringReader(privateKeyPem)).readPemObject()
        val keySpec = PKCS8EncodedKeySpec(pemContent.content)
        return keyFactory.generatePrivate(keySpec)
    }

    private fun loadPublicKey(): PublicKey {
        val publicKeyPem = config.publicKeyFile.readText()
        val keyFactory = KeyFactory.getInstance("RSA", "BC")
        val pemContent = PemReader(StringReader(publicKeyPem)).readPemObject()
        val keySpec = X509EncodedKeySpec(pemContent.content)
        return keyFactory.generatePublic(keySpec)
    }


    fun signData(data: String): String {
        val privateKey = loadPrivateKey()
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
        responseBody: String,
        signature: String,
    ): Boolean {
        return try {
            val publicKey = loadPublicKey()
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
}
