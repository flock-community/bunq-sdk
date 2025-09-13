package com.bunq.sdk

import org.junit.jupiter.api.Assertions.assertNotNull
import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.assertDoesNotThrow
import java.io.File

class RsaKeyPairGeneratorTest {

    @Test
    fun `generateKeyPair should create valid RSA key pair with private and public keys`() {
        val (private, public) = RsaKeyPairGenerator.generateRsaKeyPair()

        assertNotNull(private)
        assertNotNull(public)
    }

    @Test
    fun `generate key pair and write PEM files should return valid PEM format`() {
        val publicKeyFile = File("../../public_key.pem").apply { deleteOnExit() }
        val privateKeyFile = File("../../private_key.pem").apply { deleteOnExit() }
        RsaKeyPairGenerator.generateRsaKeyPair(privateKeyFile, publicKeyFile)

        val publicKeyString = publicKeyFile.readText()
        val privateKeyString = privateKeyFile.readText()
        assertNotNull(publicKeyString)
        assertTrue(publicKeyString.startsWith("-----BEGIN PUBLIC KEY-----"))
        assertTrue(publicKeyString.endsWith("-----END PUBLIC KEY-----\n"))

        assertDoesNotThrow {
            Config(
                bunqServer = BUNQ_PUBLIC_SERVER,
                serviceName = "test",
                apiKey = "test",
                privateKeyPem = privateKeyString,
                publicKeyPem = publicKeyString
            )
        }

    }
}