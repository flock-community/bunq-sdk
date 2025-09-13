package com.bunq.sdk

import org.bouncycastle.jce.provider.BouncyCastleProvider
import org.bouncycastle.util.io.pem.PemReader
import java.io.StringReader
import java.security.KeyFactory
import java.security.Security
import java.security.interfaces.RSAPrivateKey
import java.security.interfaces.RSAPublicKey
import java.security.spec.PKCS8EncodedKeySpec
import java.security.spec.X509EncodedKeySpec

data class BunqServer(
    val baseUrl: String,
    val pinnedKey: String,
)

val BUNQ_PUBLIC_SERVER = BunqServer(
    "https://api.bunq.com/v1/",
    "sha256/nI/T/sDfioCBHB5mVppDPyLi2HXYanwk2arpZuHLOu0="
)

val BUNQ_SANDBOX_SERVER = BunqServer(
    "https://public-api.sandbox.bunq.com/v1/",
    "sha256/++MBgDH5WGvL9Bcn5Be30cRcL0f5O+NyoXuWtQdX1aI="
)


/**
 * Configuration class for a bunq API client containing all necessary settings and credentials
 * for establishing and managing API connections.
 *
 * All parameters are validated upon construction to ensure proper format and compatibility.
 */
data class Config(
    /** The bunq API server configuration including base URL and pinned key */
    val bunqServer: BunqServer,
    /** Name of the service/application using the bunq API */
    val serviceName: String,
    /** API key for authentication with bunq servers */
    val apiKey: String,
    /** Private key in PEM format for signing API requests */
    private val privateKeyPem: String,
    /** Public key in PEM format for API request verification */
    private val publicKeyPem: String,
    /** Custom user agent string for API requests */
    val userAgent: String? = null,
    /** Cache control header value for API requests */
    val cacheControl: String? = null,
    /** Preferred language for API responses */
    val language: String? = null,
    /** Geographic region for API requests */
    val region: String? = null,
    /** Custom client request ID for tracking API calls */
    val clientRequestId: String? = null,
    /** Geolocation information for API requests */
    val geolocation: String? = null,
) {
    val privateKey: RSAPrivateKey
    val publicKey: RSAPublicKey

    init {
        require(serviceName.isNotBlank()) { "Service name cannot be blank" }
        require(apiKey.isNotBlank()) { "API key cannot be blank" }

        privateKey = validateAndLoadPrivateKey(privateKeyPem)
        publicKey = validateAndLoadPublicKey(publicKeyPem)

        validateKeyCompatibility(privateKey, publicKey)
    }

    fun getPublicKeyAsString(): String = publicKeyPem
}

private fun validateAndLoadPrivateKey(privateKeyPem: String): RSAPrivateKey {
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

private fun validateAndLoadPublicKey(publicKeyPem: String): RSAPublicKey {
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

private fun validateKeyCompatibility(privateKey: RSAPrivateKey, publicKey: RSAPublicKey) {
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
