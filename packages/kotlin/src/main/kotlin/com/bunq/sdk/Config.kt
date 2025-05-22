package com.bunq.sdk

import java.io.File

data class Config(
    val serviceName: String,
    val apiKey: String,
    val privateKeyFile: File = File("../private_key.pem"),
    val publicKeyFile:File = File("../public_key.pem")
)
