package com.bunq.sdk

import org.junit.jupiter.api.Test
import java.io.File
import kotlin.test.assertEquals


class SigningTest {

    @Test
    fun signing() {

        val config = Config(
            bunqServer = BUNQ_SANDBOX_SERVER,
            serviceName = "",
            apiKey = "",
            publicKeyFile = File("../../test/public_key.pem"),
            privateKeyFile = File("../../test/private_key.pem"),

        )
        val signing = Signing(config)
        val res = signing.signData("Hello")
        assertEquals(
            "fR0Gyn8VfC8eCwq10x5eYAcxXh4nv6331hWAAr77l72zfFScbw3hFSE6iBNklCYc0mfnKezsuRo3re+fTNNHO1oZhfhjc9i4UYxTxBiOEslHrKx9NkXkBZh2RALx/LnhlpyMwB5BBOlFlNeR9Hyj5E8c/a2pObBZRmrZ3cgAnoWF8hhY5Y9XwLS2WIodYIPSQXuQMXyi1UBxhxAbniZ5m1uRSt8gaPmQGMCQtUzvZ8KUXtSvugGPsXHwh94EccZCfjS0sdIQK8AcZ8t5YL6bqkqJ7eVzbxoX6U1nOZVy3MxQMKQ/PFS297er6qsVsGwKbNfaTUvymEb46mM/gQdQDQ==",
            res
        )
    }
}