package com.bunq.sdk

import org.bouncycastle.jce.provider.BouncyCastleProvider
import org.bouncycastle.util.io.pem.PemObject
import org.bouncycastle.util.io.pem.PemWriter
import java.io.File
import java.io.StringWriter
import java.security.KeyPairGenerator
import java.security.PrivateKey
import java.security.PublicKey
import java.security.SecureRandom
import java.security.Security

object RsaKeyPairGenerator {
    val keyPairGenerator: KeyPairGenerator

    init {
        if (Security.getProvider("BC") == null) {
            Security.addProvider(BouncyCastleProvider())
        }

        keyPairGenerator = KeyPairGenerator.getInstance("RSA", "BC")
        keyPairGenerator.initialize(2048, SecureRandom())
    }

    /**
     * Generates an RSA key pair consisting of a private key and a public key, both encoded in PEM format.
     *
     * @return A pair containing the private key as the first element and the public key as the second element,
     * both represented as strings in PEM format.
     */
    fun generateRsaKeyPair(): Pair<String, String> {
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