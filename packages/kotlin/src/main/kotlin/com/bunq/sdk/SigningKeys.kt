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

internal fun validateAndLoadPrivateKey(privateKeyPem: String): RSAPrivateKey {
    rejectUnsupportedPrivateKeyFormat(privateKeyPem)
    val der = readPemBody(privateKeyPem, "PRIVATE KEY", "PKCS#8", KeyType.PRIVATE)
    try {
        ensureBouncyCastleProvider()
        return KeyFactory.getInstance("RSA", "BC").generatePrivate(PKCS8EncodedKeySpec(der)) as RSAPrivateKey
    } catch (e: Exception) {
        throw InvalidRsaKeyException(
            "Private key is not a valid RSA key (RSA_VALIDATION): ${e.message}. " +
                "Only RSA keys are supported; generate one with: openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048",
            KeyType.PRIVATE, cause = e,
        )
    }
}

internal fun validateAndLoadPublicKey(publicKeyPem: String): RSAPublicKey {
    val der = readPemBody(publicKeyPem, "PUBLIC KEY", "X.509 SubjectPublicKeyInfo", KeyType.PUBLIC)
    try {
        ensureBouncyCastleProvider()
        return KeyFactory.getInstance("RSA", "BC").generatePublic(X509EncodedKeySpec(der)) as RSAPublicKey
    } catch (e: Exception) {
        throw InvalidRsaKeyException(
            "Public key is not a valid RSA key (RSA_VALIDATION): ${e.message}. " +
                "Only RSA keys are supported; derive it with: openssl rsa -in private_key_pkcs8.pem -pubout -out public_key.pem",
            KeyType.PUBLIC, cause = e,
        )
    }
}

private fun rejectUnsupportedPrivateKeyFormat(pem: String) {
    when {
        pem.contains("ENCRYPTED PRIVATE KEY") || pem.contains("Proc-Type: 4,ENCRYPTED") ->
            throw InvalidPemFormatException(
                "Private key is encrypted (PEM_PARSING); encrypted keys are not supported. " +
                    "Decrypt it first, e.g.: openssl pkcs8 -topk8 -nocrypt -in encrypted_key.pem -out private_key_pkcs8.pem",
                KeyType.PRIVATE,
            )

        pem.contains("-----BEGIN RSA PRIVATE KEY-----") ->
            throw InvalidPemFormatException(
                "Private key is in PKCS#1 format (PEM_PARSING) but PKCS#8 ('-----BEGIN PRIVATE KEY-----') is required. " +
                    "Convert it with: $PKCS8_FIX",
                KeyType.PRIVATE,
            )
    }
}

private fun readPemBody(pem: String, label: String, format: String, keyType: KeyType): ByteArray {
    val which = keyType.name.lowercase()
    val begin = "-----BEGIN $label-----"
    val end = "-----END $label-----"
    if (!pem.contains(begin) || !pem.contains(end)) {
        val problem = if (pem.contains(begin)) "the '$end' line is missing, the PEM looks truncated"
        else "expected a $format PEM starting with '$begin'"
        throw InvalidPemFormatException("Invalid $which key PEM (PEM_PARSING): $problem", keyType)
    }
    try {
        return PemReader(StringReader(pem)).readPemObject().content
    } catch (e: Exception) {
        throw InvalidPemFormatException(
            "Invalid $which key PEM (PEM_PARSING): the body is not valid base64 or is malformed (${e.message}). " +
                "Re-export the key without modifying it.",
            keyType, cause = e,
        )
    }
}

internal fun validateKeyCompatibility(privateKey: RSAPrivateKey, publicKey: RSAPublicKey) {
    try {
        // Verify that the private and public keys are a matching pair
        // by checking that they have the same modulus
        if (privateKey.modulus != publicKey.modulus) {
            throw KeyMismatchException(
                "Private and public key do not match (COMPATIBILITY_CHECK): the moduli differ. " +
                    "Derive the public key from the private key: openssl rsa -in private_key_pkcs8.pem -pubout -out public_key.pem"
            )
        }

        // Additional check: verify that the public exponent matches the expected value for RSA
        if (publicKey.publicExponent.toLong() != 65537L) {
            throw InvalidRsaKeyException(
                "Public key has unexpected exponent (COMPATIBILITY_CHECK). Expected 65537, got ${publicKey.publicExponent}",
                KeyType.PUBLIC, ValidationStage.COMPATIBILITY_CHECK,
            )
        }

    } catch (e: Exception) {
        when (e) {
            is ConfigValidationException -> throw e
            else -> throw KeyMismatchException("Failed to validate key compatibility (COMPATIBILITY_CHECK): ${e.message}")
        }
    }
}

private fun ensureBouncyCastleProvider() {
    if (Security.getProvider("BC") == null) {
        Security.addProvider(BouncyCastleProvider())
    }
}