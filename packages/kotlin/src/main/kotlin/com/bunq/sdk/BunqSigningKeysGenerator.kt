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
import java.security.interfaces.RSAPrivateKey
import java.security.interfaces.RSAPublicKey

object BunqSigningKeysGenerator {
    private val keyPairGenerator: KeyPairGenerator

    init {
        if (Security.getProvider("BC") == null) {
            Security.addProvider(BouncyCastleProvider())
        }

        keyPairGenerator = KeyPairGenerator.getInstance("RSA", "BC")
        keyPairGenerator.initialize(2048, SecureRandom())
    }

    /**
     * Generates an RSA key pair using 2048-bit key size.
     *
     * @return A KeyPair containing the generated private and public keys.
     */
    fun generateBunqSigningKeys(): SigningKeys {
        val keyPair = keyPairGenerator.generateKeyPair()
        println("bunq - created new keypair [KEEP IT SAFE]")
        return SigningKeys.FromRSAKeys(keyPair.private as RSAPrivateKey, keyPair.public as RSAPublicKey)

    }

    /**
     * Generates and stores an RSA key pair in the specified files. If the files already exist,
     * the existing key pair will be reused. The key pair is generated using a 2048-bit key size.
     *
     * @param privateKeyFile The file where the generated private key will be stored or retrieved from if it already exists.
     * @param publicKeyFile The file where the generated public key will be stored or retrieved from if it already exists.
     */
    fun generateBunqSigningKeys(privateKeyFile: File, publicKeyFile: File): SigningKeys {
        if (privateKeyFile.exists() && publicKeyFile.exists()) {
            println("bunq - using existing keypair")
            return SigningKeys.FromPem(privateKeyFile.readText(), publicKeyFile.readText())
        }

        val signingKeys = generateBunqSigningKeys()
        privateKeyFile.writeText(signingKeys.privateKeyAsPem())
        publicKeyFile.writeText(signingKeys.publicKeyAsPem())

        println("bunq - created new keypair [KEEP THESE FILES SAFE]")
        return signingKeys
    }

    internal fun convertPrivateKeyToPem(privateKey: PrivateKey): String {
        return StringWriter().use { stringWriter ->
            PemWriter(stringWriter).use { pemWriter ->
                pemWriter.writeObject(PemObject("PRIVATE KEY", privateKey.encoded))
            }
            stringWriter.toString()
        }
    }

    internal fun convertPublicKeyToPem(publicKey: PublicKey): String {
        return StringWriter().use { stringWriter ->
            PemWriter(stringWriter).use { pemWriter ->
                pemWriter.writeObject(PemObject("PUBLIC KEY", publicKey.encoded))
            }
            stringWriter.toString()
        }
    }
}