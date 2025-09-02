package com.bunq.sdk

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
 * Configuration class for bunq API client containing all necessary settings and credentials
 * for establishing and managing API connections.
 */
data class Config(
    /** The bunq API server configuration including base URL and pinned key */
    val bunqServer: BunqServer,
    /** Name of the service/application using the bunq API */
    val serviceName: String,
    /** API key for authentication with bunq servers */
    val apiKey: String,
    /** Private key in PEM format for signing API requests */
    val privateKeyPem: String,
    /** Public key in PEM format for API request verification */
    val publicKeyPem: String,
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
)
