package com.bunq.sdk

import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.assertDoesNotThrow
import java.io.File

class BunqSigningKeysGeneratorTest {

    @Test
    fun `generateKeyPair should create valid RSA key pair with private and public keys`() {
        val keyPair = assertDoesNotThrow {
            BunqSigningKeysGenerator.generateBunqSigningKeys()
        }
        assertTrue { keyPair.privateKey().algorithm == "RSA" }
        assertTrue { keyPair.publicKey().algorithm == "RSA" }
        assertTrue { keyPair.privateKey().encoded.isNotEmpty() }
        assertTrue { keyPair.publicKey().encoded.isNotEmpty() }
        assertTrue { keyPair.privateKey().format == "PKCS#8" }
        assertTrue { keyPair.publicKey().format == "X.509" }
        assertTrue { keyPair.privateKey().encoded.size > 1024 }
        assertTrue { keyPair.privateKey().modulus.bitLength() >= 2048 }
        assertTrue { keyPair.privateKey().privateExponent.toLong() != 65537L }
        assertTrue { keyPair.publicKey().modulus.bitLength() == keyPair.privateKey().modulus.bitLength() }
        assertTrue { keyPair.publicKey().publicExponent.toLong() == 65537L }

        assertTrue { keyPair.publicKeyAsPem().startsWith("-----BEGIN PUBLIC KEY-----") }
        assertTrue { keyPair.publicKeyAsPem().endsWith("-----END PUBLIC KEY-----\n") }

        assertTrue { keyPair.privateKeyAsPem().startsWith("-----BEGIN PRIVATE KEY-----") }
        assertTrue { keyPair.privateKeyAsPem().endsWith("-----END PRIVATE KEY-----\n") }
    }

    @Test
    fun `generate key pair and write PEM files should return valid PEM format`() {
        val publicKeyFile = File("../../public_key.pem").apply { deleteOnExit() }
        val privateKeyFile = File("../../private_key.pem").apply { deleteOnExit() }
        val generatedRsaKeyPair = BunqSigningKeysGenerator.generateBunqSigningKeys(privateKeyFile, publicKeyFile)

        val publicKeyString = publicKeyFile.readText()
        val privateKeyString = privateKeyFile.readText()

        assertTrue { generatedRsaKeyPair.privateKeyAsPem() == privateKeyString }
        assertTrue { generatedRsaKeyPair.publicKeyAsPem() == publicKeyString }

        assertTrue(publicKeyString.startsWith("-----BEGIN PUBLIC KEY-----"))
        assertTrue(publicKeyString.endsWith("-----END PUBLIC KEY-----\n"))

        assertTrue { privateKeyString.startsWith("-----BEGIN PRIVATE KEY-----") }
        assertTrue { privateKeyString.endsWith("-----END PRIVATE KEY-----\n") }
    }
}