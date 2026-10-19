package com.bunq.sdk

import java.time.Instant
import kotlin.test.Test
import kotlin.test.assertFalse
import kotlin.test.assertTrue

class SecretMaskingTest {

    @Test
    fun `toString masks secrets and keeps non-secret fields`() {
        val keys = BunqSigningKeysGenerator.generateBunqSigningKeys()
        val config = Config(BUNQ_SANDBOX_SERVER, "my-service", "secret-api-key", keys)
        val context = Context("server-key", 1, 2, "secret-session", 3, Instant.EPOCH, "secret-install", config)

        val text = context.toString()

        listOf("secret-api-key", "secret-session", "secret-install", keys.privateKeyAsPem().lines()[1])
            .forEach { assertFalse(text.contains(it), it) }
        assertTrue(text.contains("my-service"))
        assertTrue(text.contains("userId=3"))
    }
}
