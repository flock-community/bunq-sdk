package com.bunq.sdk

import com.bunq.sdk.BunqSigningKeysGenerator.convertPrivateKeyToPem
import com.bunq.sdk.BunqSigningKeysGenerator.convertPublicKeyToPem
import org.bouncycastle.jce.provider.BouncyCastleProvider
import org.bouncycastle.util.io.pem.PemReader
import java.io.StringReader
import java.security.KeyFactory
import java.security.Security
import java.security.interfaces.RSAPrivateKey
import java.security.interfaces.RSAPublicKey
import java.security.spec.PKCS8EncodedKeySpec
import java.security.spec.X509EncodedKeySpec

/**
 * Sealed class hierarchy for RSA key pairs used in bunq API request signing.
 * 
 * Provides consistent access to both PEM string representations and parsed 
 * RSA key objects, ensuring they remain synchronized.
 * 
 * Available implementations:
 * - [FromPem] - Load from PEM strings (most common)
 * - [FromRSAKeys] - Wrap existing RSA key objects  
 */
sealed interface SigningKeys {
    fun privateKeyAsPem(): String
    fun publicKeyAsPem(): String
    fun privateKey(): RSAPrivateKey
    fun publicKey(): RSAPublicKey


    class FromPem(
        private val privateKeyAsPem: String,
        private val publicKeyAsPem: String
    ) : SigningKeys {
        private val privateKey: RSAPrivateKey = validateAndLoadPrivateKey(privateKeyAsPem)
        private val publicKey: RSAPublicKey = validateAndLoadPublicKey(publicKeyAsPem)

        init {
            validateKeyCompatibility(privateKey, publicKey)
        }

        override fun privateKeyAsPem(): String = privateKeyAsPem
        override fun publicKeyAsPem(): String = publicKeyAsPem
        override fun privateKey(): RSAPrivateKey = privateKey
        override fun publicKey(): RSAPublicKey = publicKey
    }

    class FromRSAKeys(
        val privateKey: RSAPrivateKey,
        val publicKey: RSAPublicKey
    ) : SigningKeys {
        private val privateKeyAsPem: String = convertPrivateKeyToPem(privateKey)
        private val publicKeyAsPem: String = convertPublicKeyToPem(publicKey)

        init {
            validateKeyCompatibility(privateKey, publicKey)
        }

        override fun privateKeyAsPem(): String = privateKeyAsPem
        override fun publicKeyAsPem(): String = publicKeyAsPem
        override fun privateKey(): RSAPrivateKey = privateKey
        override fun publicKey(): RSAPublicKey = publicKey
    }
}


private const val PKCS8_FIX =
    "openssl pkcs8 -topk8 -inform PEM -outform PEM -nocrypt -in private_key.pem -out private_key_pkcs8.pem"
private const val PUBLIC_FROM_PRIVATE_FIX = "openssl rsa -in private_key_pkcs8.pem -pubout -out public_key.pem"

internal fun validateAndLoadPrivateKey(privateKeyPem: String): RSAPrivateKey {
    rejectUnsupportedPrivateKeyFormat(privateKeyPem)
    val der = readPemBody(privateKeyPem, "PRIVATE KEY", KeyType.PRIVATE)
    try {
        ensureBouncyCastleProvider()
        return KeyFactory.getInstance("RSA", "BC").generatePrivate(PKCS8EncodedKeySpec(der)) as RSAPrivateKey
    } catch (e: Exception) {
        throw InvalidRsaKeyException(
            "not a valid RSA key (${e.message}). " +
                "Only RSA keys are supported; generate one with: openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048",
            KeyType.PRIVATE, e,
        )
    }
}

internal fun validateAndLoadPublicKey(publicKeyPem: String): RSAPublicKey {
    rejectUnsupportedPublicKeyFormat(publicKeyPem)
    val der = readPemBody(publicKeyPem, "PUBLIC KEY", KeyType.PUBLIC)
    try {
        ensureBouncyCastleProvider()
        return KeyFactory.getInstance("RSA", "BC").generatePublic(X509EncodedKeySpec(der)) as RSAPublicKey
    } catch (e: Exception) {
        throw InvalidRsaKeyException(
            "not a valid RSA key (${e.message}). Only RSA keys are supported; derive it with: $PUBLIC_FROM_PRIVATE_FIX",
            KeyType.PUBLIC, e,
        )
    }
}

private fun rejectUnsupportedPrivateKeyFormat(pem: String) {
    when {
        pem.contains("ENCRYPTED PRIVATE KEY") || pem.contains("Proc-Type: 4,ENCRYPTED") ->
            throw InvalidPemFormatException(
                "the key is encrypted, which is not supported. Decrypt it first (the command asks for the passphrase): " +
                    "openssl pkcs8 -topk8 -nocrypt -in encrypted_key.pem -out private_key_pkcs8.pem",
                KeyType.PRIVATE,
            )

        pem.contains("-----BEGIN RSA PRIVATE KEY-----") ->
            throw InvalidPemFormatException(
                "the key is in PKCS#1 format but PKCS#8 ('-----BEGIN PRIVATE KEY-----') is required. Convert it with: $PKCS8_FIX",
                KeyType.PRIVATE,
            )

        pem.contains("-----BEGIN PUBLIC KEY-----") || pem.contains("-----BEGIN RSA PUBLIC KEY-----") ->
            throw InvalidPemFormatException(
                "this is a public key, a private key is expected. The keys may be swapped.",
                KeyType.PRIVATE,
            )
    }
}

private fun rejectUnsupportedPublicKeyFormat(pem: String) {
    when {
        pem.contains("-----BEGIN RSA PUBLIC KEY-----") ->
            throw InvalidPemFormatException(
                "the key is in PKCS#1 format but X.509 ('-----BEGIN PUBLIC KEY-----') is required. Convert it with: " +
                    "openssl rsa -RSAPublicKey_in -in public_key.pem -pubout -out public_key_spki.pem",
                KeyType.PUBLIC,
            )

        pem.contains("PRIVATE KEY-----") ->
            throw InvalidPemFormatException(
                "this is a private key, a public key is expected. The keys may be swapped. " +
                    "Derive the public key with: $PUBLIC_FROM_PRIVATE_FIX",
                KeyType.PUBLIC,
            )
    }
}

private fun readPemBody(pem: String, label: String, keyType: KeyType): ByteArray {
    val begin = "-----BEGIN $label-----"
    val end = "-----END $label-----"
    fun invalid(detail: String, cause: Throwable? = null): Nothing =
        throw InvalidPemFormatException(detail, keyType, cause)

    if (!pem.contains(begin)) invalid("expected a PEM starting with '$begin'")
    if (!pem.contains(end)) invalid("the '$end' line is missing, the PEM looks truncated")
    if (pem.contains("\\n")) invalid("the PEM contains literal \\n sequences; replace them with real newlines")
    if (!pem.trim().contains('\n')) invalid("the PEM has no line breaks; put the BEGIN line, the base64 body and the END line on separate lines")

    val block = try {
        PemReader(StringReader(pem)).readPemObject()
    } catch (e: Exception) {
        invalid("the body is not valid base64 or is malformed (${e.message}). Re-export the key without modifying it.", e)
    } ?: invalid("no PEM block could be read; check that no line is indented and all line breaks are real newlines")

    if (block.type != label) invalid("the first PEM block is '${block.type}' but '$label' is expected")
    return block.content
}

internal fun validateKeyCompatibility(privateKey: RSAPrivateKey, publicKey: RSAPublicKey) {
    if (publicKey.publicExponent.toLong() != 65537L) {
        throw InvalidRsaKeyException("unexpected public exponent. Expected 65537, got ${publicKey.publicExponent}", KeyType.PUBLIC)
    }
    if (privateKey.modulus != publicKey.modulus) {
        throw KeyMismatchException("the keys do not form a pair (the moduli differ). Derive the public key with: $PUBLIC_FROM_PRIVATE_FIX")
    }
}

private fun ensureBouncyCastleProvider() {
    if (Security.getProvider("BC") == null) {
        Security.addProvider(BouncyCastleProvider())
    }
}