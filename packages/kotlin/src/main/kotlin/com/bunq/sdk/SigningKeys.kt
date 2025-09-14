package com.bunq.sdk

import com.bunq.sdk.BunqSigningKeysGenerator.convertPrivateKeyToPem
import com.bunq.sdk.BunqSigningKeysGenerator.convertPublicKeyToPem
import org.bouncycastle.jce.provider.BouncyCastleProvider
import org.bouncycastle.util.io.pem.PemReader
import java.io.StringReader
import java.security.KeyFactory
import java.security.Security
import java.security.interfaces.RSAPrivateKey
import java.security.interfaces.RSAPublicKey
import java.security.spec.PKCS8EncodedKeySpec
import java.security.spec.X509EncodedKeySpec

/**
 * Sealed class hierarchy for RSA key pairs used in bunq API request signing.
 * 
 * Provides consistent access to both PEM string representations and parsed 
 * RSA key objects, ensuring they remain synchronized.
 * 
 * Available implementations:
 * - [FromPem] - Load from PEM strings (most common)
 * - [FromRSAKeys] - Wrap existing RSA key objects  
 */
sealed interface SigningKeys {
    fun privateKeyAsPem(): String
    fun publicKeyAsPem(): String
    fun privateKey(): RSAPrivateKey
    fun publicKey(): RSAPublicKey


    class FromPem(
        private val privateKeyAsPem: String,
        private val publicKeyAsPem: String
    ) : SigningKeys {
        private val privateKey: RSAPrivateKey = validateAndLoadPrivateKey(privateKeyAsPem)
        private val publicKey: RSAPublicKey = validateAndLoadPublicKey(publicKeyAsPem)

        init {
            validateKeyCompatibility(privateKey, publicKey)
        }

        override fun privateKeyAsPem(): String = privateKeyAsPem
        override fun publicKeyAsPem(): String = publicKeyAsPem
        override fun privateKey(): RSAPrivateKey = privateKey
        override fun publicKey(): RSAPublicKey = publicKey
    }

    class FromRSAKeys(
        val privateKey: RSAPrivateKey,
        val publicKey: RSAPublicKey
    ) : SigningKeys {
        private val privateKeyAsPem: String = convertPrivateKeyToPem(privateKey)
        private val publicKeyAsPem: String = convertPublicKeyToPem(publicKey)

        init {
            validateKeyCompatibility(privateKey, publicKey)
        }

        override fun privateKeyAsPem(): String = privateKeyAsPem
        override fun publicKeyAsPem(): String = publicKeyAsPem
        override fun privateKey(): RSAPrivateKey = privateKey
        override fun publicKey(): RSAPublicKey = publicKey
    }
}


internal fun validateAndLoadPrivateKey(privateKeyPem: String): RSAPrivateKey {
    try {
        if (!privateKeyPem.contains("-----BEGIN PRIVATE KEY-----") ||
            !privateKeyPem.contains("-----END PRIVATE KEY-----")
        ) {
            throw InvalidPemFormatException("Private key must be in PKCS#8 PEM format")
        }

        ensureBouncyCastleProvider()
        val keyFactory = KeyFactory.getInstance("RSA", "BC")
        val pemReader = PemReader(StringReader(privateKeyPem))
        val pemContent = pemReader.readPemObject()
            ?: throw InvalidPemFormatException("Could not parse private key PEM content")

        val keySpec = PKCS8EncodedKeySpec(pemContent.content)
        val privateKey = keyFactory.generatePrivate(keySpec)

        if (privateKey !is RSAPrivateKey) {
            throw InvalidRsaKeyException("Private key must be an RSA key")
        }

        return privateKey
    } catch (e: Exception) {
        when (e) {
            is ConfigValidationException -> throw e
            else -> throw InvalidRsaKeyException("Failed to load private key: ${e.message}", e)
        }
    }
}

internal fun validateAndLoadPublicKey(publicKeyPem: String): RSAPublicKey {
    try {
        if (!publicKeyPem.contains("-----BEGIN PUBLIC KEY-----") ||
            !publicKeyPem.contains("-----END PUBLIC KEY-----")
        ) {
            throw InvalidPemFormatException("Public key must be in X.509 PEM format")
        }

        ensureBouncyCastleProvider()
        val keyFactory = KeyFactory.getInstance("RSA", "BC")
        val pemReader = PemReader(StringReader(publicKeyPem))
        val pemContent = pemReader.readPemObject()
            ?: throw InvalidPemFormatException("Could not parse public key PEM content")

        val keySpec = X509EncodedKeySpec(pemContent.content)
        val publicKey = keyFactory.generatePublic(keySpec)

        if (publicKey !is RSAPublicKey) {
            throw InvalidRsaKeyException("Public key must be an RSA key")
        }

        return publicKey
    } catch (e: Exception) {
        when (e) {
            is ConfigValidationException -> throw e
            else -> throw InvalidRsaKeyException("Failed to load public key: ${e.message}", e)
        }
    }
}

internal fun validateKeyCompatibility(privateKey: RSAPrivateKey, publicKey: RSAPublicKey) {
    try {
        // Verify that the private and public keys are a matching pair
        // by checking that they have the same modulus
        if (privateKey.modulus != publicKey.modulus) {
            throw KeyMismatchException("Private and public keys do not form a valid key pair (modulus mismatch)")
        }

        // Additional check: verify that the public exponent matches the expected value for RSA
        if (publicKey.publicExponent.toLong() != 65537L) {
            throw InvalidRsaKeyException("Public key has unexpected exponent. Expected 65537, got ${publicKey.publicExponent}")
        }

    } catch (e: Exception) {
        when (e) {
            is ConfigValidationException -> throw e
            else -> throw KeyMismatchException("Failed to validate key compatibility: ${e.message}")
        }
    }
}

private fun ensureBouncyCastleProvider() {
    if (Security.getProvider("BC") == null) {
        Security.addProvider(BouncyCastleProvider())
    }
}