package com.bunq.sdk

import java.io.File

data class Config(
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
