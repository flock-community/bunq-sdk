package com.bunq.sdk

import org.bouncycastle.jce.provider.BouncyCastleProvider
import org.bouncycastle.util.io.pem.PemObject
import org.bouncycastle.util.io.pem.PemReader
import org.bouncycastle.util.io.pem.PemWriter
import java.io.File
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


object Signing{
    init {
        if (Security.getProvider("BC") == null) {
            Security.addProvider(BouncyCastleProvider())
        }
    }

    fun signData(config: Config, data: String): String {
        val privateKey = loadPrivateKey(config)
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
        val publicKey = loadPublicKey(config)
        val decodedSignature = Base64.getDecoder().decode(signature)

        val verifier = Signature.getInstance("SHA256withRSA", "BC")
        verifier.initVerify(publicKey)
        verifier.update(responseBody.toByteArray(Charsets.UTF_8))

        verifier.verify(decodedSignature)
    } catch (e: Exception) {
        println("[ERROR] Signature verification failed: ${e.message}")
        false
    }

    private fun loadPublicKey(config: Config): PublicKey {
        val keyFactory = KeyFactory.getInstance("RSA", "BC")
        val pemContent = PemReader(StringReader(config.publicKeyPem)).readPemObject()
        val keySpec = X509EncodedKeySpec(pemContent.content)
        return keyFactory.generatePublic(keySpec)
    }


    private fun loadPrivateKey(config: Config): PrivateKey {
        val keyFactory = KeyFactory.getInstance("RSA", "BC")
        val pemReader = PemReader(StringReader(config.privateKeyPem))
        val pemContent = pemReader.readPemObject()
        val keySpec = PKCS8EncodedKeySpec(pemContent.content)
        return keyFactory.generatePrivate(keySpec)
    }
}


object RsaKeyPairGenerator {
    init {
        if (Security.getProvider("BC") == null) {
            Security.addProvider(BouncyCastleProvider())
        }
    }

    /**
     * Generates an RSA key pair consisting of a private key and a public key, both encoded in PEM format.
     *
     * @return A pair containing the private key as the first element and the public key as the second element,
     * both represented as strings in PEM format.
     */
    fun generateRsaKeyPair(): Pair<String, String> {
        val keyPairGenerator = KeyPairGenerator.getInstance("RSA", "BC")
        keyPairGenerator.initialize(2048, SecureRandom())
        val keyPair = keyPairGenerator.generateKeyPair()

        val privateKeyPem = convertPrivateKeyToPem(keyPair.private)
        val publicKeyPem = convertPublicKeyToPem(keyPair.public)

        println("bunq - created new keypair [KEEP THESE FILES SAFE]")
        return Pair(privateKeyPem, publicKeyPem)
    }

    /**
     * Generates and stores an RSA key pair in the specified files. If the files already exist,
     * the existing key pair will be reused. The key pair is generated using a 2048-bit key size.
     *
     * @param privateKeyFile The file where the generated private key will be stored or retrieved from if it already exists.
     * @param publicKeyFile The file where the generated public key will be stored or retrieved from if it already exists.
     */
    fun generateRsaKeyPair(privateKeyFile: File, publicKeyFile: File) {
        if (privateKeyFile.exists() && publicKeyFile.exists()) {
            println("bunq - using existing keypair")
        }

        val keyPairGenerator = KeyPairGenerator.getInstance("RSA", "BC")
        keyPairGenerator.initialize(2048, SecureRandom())
        val keyPair = keyPairGenerator.generateKeyPair()

        val privateKeyPem = convertPrivateKeyToPem(keyPair.private)
        val publicKeyPem = convertPublicKeyToPem(keyPair.public)

        privateKeyFile.writeText(privateKeyPem)
        publicKeyFile.writeText(publicKeyPem)

        println("bunq - created new keypair [KEEP THESE FILES SAFE]")
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
}
