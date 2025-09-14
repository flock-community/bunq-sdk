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
    /** Key pair for server-side request signing */
    val signingKeys: SigningKeys,
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
    init {
        require(serviceName.isNotBlank()) { "Service name cannot be blank" }
        require(apiKey.isNotBlank()) { "API key cannot be blank" }

    }
}

