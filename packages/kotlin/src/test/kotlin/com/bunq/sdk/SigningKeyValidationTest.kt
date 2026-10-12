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
        println("MESSAGE[$phrase]: ${e.message}")
    }

    @Test
    fun `PKCS1 private key gets openssl conversion command`() {
        val pkcs1 = PrivateKeyInfo.getInstance(valid.privateKey().encoded).parsePrivateKey().toASN1Primitive().encoded
        assertFailure<InvalidPemFormatException>(KeyType.PRIVATE, ValidationStage.PEM_PARSING, "Private key validation failed during PEM parsing: the key is in PKCS#1 format") {
            SigningKeys.FromPem(pem("RSA PRIVATE KEY", pkcs1), valid.publicKeyAsPem())
        }
    }

    @Test
    fun `encrypted private key is rejected`() {
        val encrypted = pem("ENCRYPTED PRIVATE KEY", valid.privateKey().encoded)
        assertFailure<InvalidPemFormatException>(KeyType.PRIVATE, ValidationStage.PEM_PARSING, "the command asks for the passphrase") {
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
        assertFailure<InvalidRsaKeyException>(KeyType.PRIVATE, ValidationStage.RSA_VALIDATION, "Private key validation failed during RSA validation") {
            SigningKeys.FromPem(pem("PRIVATE KEY", ec.private.encoded), valid.publicKeyAsPem())
        }
    }

    @Test
    fun `mismatched key pair is reported for both keys`() {
        val other = BunqSigningKeysGenerator.generateBunqSigningKeys()
        assertFailure<KeyMismatchException>(KeyType.BOTH, ValidationStage.COMPATIBILITY_CHECK, "Private and public key validation failed during compatibility check") {
            SigningKeys.FromPem(valid.privateKeyAsPem(), other.publicKeyAsPem())
        }
    }

    @Test
    fun `PKCS1 conversion command is included`() {
        val pkcs1 = PrivateKeyInfo.getInstance(valid.privateKey().encoded).parsePrivateKey().toASN1Primitive().encoded
        assertFailure<InvalidPemFormatException>(KeyType.PRIVATE, ValidationStage.PEM_PARSING, "openssl pkcs8 -topk8 -inform PEM -outform PEM -nocrypt -in private_key.pem -out private_key_pkcs8.pem") {
            SigningKeys.FromPem(pem("RSA PRIVATE KEY", pkcs1), valid.publicKeyAsPem())
        }
    }

    @Test
    fun `literal backslash n is detected`() {
        val envVar = valid.privateKeyAsPem().trim().replace("\n", "\\n")
        assertFailure<InvalidPemFormatException>(KeyType.PRIVATE, ValidationStage.PEM_PARSING, "literal \\n sequences") {
            SigningKeys.FromPem(envVar, valid.publicKeyAsPem())
        }
    }

    @Test
    fun `single line PEM is detected`() {
        val oneLine = valid.publicKeyAsPem().trim().replace("\n", " ")
        assertFailure<InvalidPemFormatException>(KeyType.PUBLIC, ValidationStage.PEM_PARSING, "no line breaks") {
            SigningKeys.FromPem(valid.privateKeyAsPem(), oneLine)
        }
    }

    @Test
    fun `certificate before the key is reported as wrong block`() {
        val cert = pem("CERTIFICATE", byteArrayOf(1, 2, 3)) + valid.publicKeyAsPem()
        assertFailure<InvalidPemFormatException>(KeyType.PUBLIC, ValidationStage.PEM_PARSING, "the first PEM block is 'CERTIFICATE'") {
            SigningKeys.FromPem(valid.privateKeyAsPem(), cert)
        }
    }

    @Test
    fun `PKCS1 public key gets conversion command`() {
        val pkcs1Public = pem("RSA PUBLIC KEY", valid.publicKey().encoded)
        assertFailure<InvalidPemFormatException>(KeyType.PUBLIC, ValidationStage.PEM_PARSING, "openssl rsa -RSAPublicKey_in -in public_key.pem -pubout -out public_key_spki.pem") {
            SigningKeys.FromPem(valid.privateKeyAsPem(), pkcs1Public)
        }
    }

    @Test
    fun `public key passed as private key`() {
        assertFailure<InvalidPemFormatException>(KeyType.PRIVATE, ValidationStage.PEM_PARSING, "may be swapped") {
            SigningKeys.FromPem(valid.publicKeyAsPem(), valid.publicKeyAsPem())
        }
    }

    @Test
    fun `private key passed as public key`() {
        assertFailure<InvalidPemFormatException>(KeyType.PUBLIC, ValidationStage.PEM_PARSING, "may be swapped") {
            SigningKeys.FromPem(valid.privateKeyAsPem(), valid.privateKeyAsPem())
        }
    }

    @Test
    fun `CR only line endings load`() {
        val cr = valid.privateKeyAsPem().replace("\n", "\r")
        SigningKeys.FromPem(cr, valid.publicKeyAsPem())
    }

    @Test
    fun `trailing spaces load`() {
        val spaced = valid.privateKeyAsPem().lines().joinToString("\n") { "$it   " }
        SigningKeys.FromPem(spaced, valid.publicKeyAsPem())
    }

    @Test
    fun `indented PEM loads`() {
        val indented = valid.publicKeyAsPem().lines().joinToString("\n") { "    $it" }
        SigningKeys.FromPem(valid.privateKeyAsPem(), indented)
    }

    @Test
    fun `concatenated private and public PEM uses the first block`() {
        SigningKeys.FromPem(valid.privateKeyAsPem() + valid.publicKeyAsPem(), valid.publicKeyAsPem())
    }

    @Test
    fun `dropped body line mentions truncated or corrupted`() {
        val lines = valid.privateKeyAsPem().lines().toMutableList()
        lines.removeAt(2)
        assertFailure<InvalidRsaKeyException>(KeyType.PRIVATE, ValidationStage.RSA_VALIDATION, "may be truncated or corrupted") {
            SigningKeys.FromPem(lines.joinToString("\n"), valid.publicKeyAsPem())
        }
    }

    @Test
    fun `END line that does not match BEGIN is reported as truncated`() {
        val mismatched = valid.privateKeyAsPem().replace("-----END PRIVATE KEY-----", "-----END PUBLIC KEY-----")
        val unclosed = valid.privateKeyAsPem().replace("-----END PRIVATE KEY-----", "-----END PRIVATE KEY")
        for (pem in listOf(mismatched, unclosed)) {
            assertFailure<InvalidPemFormatException>(KeyType.PRIVATE, ValidationStage.PEM_PARSING, "the '-----END PRIVATE KEY-----' line is missing, the PEM looks truncated") {
                SigningKeys.FromPem(pem, valid.publicKeyAsPem())
            }
        }
    }
}
