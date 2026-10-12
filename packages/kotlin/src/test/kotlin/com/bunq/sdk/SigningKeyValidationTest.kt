package com.bunq.sdk

import org.bouncycastle.asn1.pkcs.PrivateKeyInfo
import org.bouncycastle.util.io.pem.PemObject
import org.bouncycastle.util.io.pem.PemWriter
import java.io.StringWriter
import java.security.KeyPairGenerator
import kotlin.test.Test
import kotlin.test.assertContains
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith

class SigningKeyValidationTest {
    private val valid = BunqSigningKeysGenerator.generateBunqSigningKeys()

    private fun pem(type: String, der: ByteArray) =
        StringWriter().also { PemWriter(it).use { w -> w.writeObject(PemObject(type, der)) } }.toString()

    private inline fun <reified T : SigningKeyValidationException> assertFailure(
        keyType: KeyType, stage: ValidationStage, phrase: String, block: () -> Unit,
    ) {
        val e = assertFailsWith<T> { block() }
        assertEquals(keyType, e.keyType)
        assertEquals(stage, e.stage)
        assertContains(e.message!!, phrase)
    }

    @Test
    fun `PKCS1 private key gets openssl conversion command`() {
        val pkcs1 = PrivateKeyInfo.getInstance(valid.privateKey().encoded).parsePrivateKey().toASN1Primitive().encoded
        assertFailure<InvalidPemFormatException>(KeyType.PRIVATE, ValidationStage.PEM_PARSING, "openssl pkcs8 -topk8 -inform PEM -outform PEM -nocrypt") {
            SigningKeys.FromPem(pem("RSA PRIVATE KEY", pkcs1), valid.publicKeyAsPem())
        }
    }

    @Test
    fun `encrypted private key is rejected`() {
        val encrypted = pem("ENCRYPTED PRIVATE KEY", valid.privateKey().encoded)
        assertFailure<InvalidPemFormatException>(KeyType.PRIVATE, ValidationStage.PEM_PARSING, "encrypted keys are not supported") {
            SigningKeys.FromPem(encrypted, valid.publicKeyAsPem())
        }
    }

    @Test
    fun `truncated PEM reports missing END line`() {
        val truncated = valid.privateKeyAsPem().substringBefore("-----END")
        assertFailure<InvalidPemFormatException>(KeyType.PRIVATE, ValidationStage.PEM_PARSING, "looks truncated") {
            SigningKeys.FromPem(truncated, valid.publicKeyAsPem())
        }
    }

    @Test
    fun `invalid base64 body is rejected`() {
        val bad = "-----BEGIN PUBLIC KEY-----\n!!!not base64!!!\n-----END PUBLIC KEY-----\n"
        assertFailure<InvalidPemFormatException>(KeyType.PUBLIC, ValidationStage.PEM_PARSING, "not valid base64") {
            SigningKeys.FromPem(valid.privateKeyAsPem(), bad)
        }
    }

    @Test
    fun `EC private key is rejected as non RSA`() {
        val ec = KeyPairGenerator.getInstance("EC").apply { initialize(256) }.generateKeyPair()
        assertFailure<InvalidRsaKeyException>(KeyType.PRIVATE, ValidationStage.RSA_VALIDATION, "Only RSA keys are supported") {
            SigningKeys.FromPem(pem("PRIVATE KEY", ec.private.encoded), valid.publicKeyAsPem())
        }
    }

    @Test
    fun `mismatched key pair is reported for both keys`() {
        val other = BunqSigningKeysGenerator.generateBunqSigningKeys()
        assertFailure<KeyMismatchException>(KeyType.BOTH, ValidationStage.COMPATIBILITY_CHECK, "do not match") {
            SigningKeys.FromPem(valid.privateKeyAsPem(), other.publicKeyAsPem())
        }
    }
}
