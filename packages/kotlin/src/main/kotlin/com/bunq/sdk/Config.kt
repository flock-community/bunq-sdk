package com.bunq.sdk

import java.io.File

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

data class Config(
    val bunqServer: BunqServer,
    val serviceName: String,
    val apiKey: String,
    val privateKeyFile: File = File("../private_key.pem"),
    val publicKeyFile: File = File("../public_key.pem"),
    val userAgent: String? = null,
    val cacheControl: String? = null,
    val language: String? = null,
    val region: String? = null,
    val clientRequestId: String? = null,
    val geolocation: String? = null,
)
