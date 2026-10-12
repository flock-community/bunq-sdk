package com.bunq.sdk

/**
 * Exception thrown when configuration validation fails
 */
sealed class ConfigValidationException(message: String, cause: Throwable? = null) : Exception(message, cause)

enum class KeyType(internal val label: String) {
    PRIVATE("Private key"),
    PUBLIC("Public key"),
    BOTH("Private and public key"),
}

enum class ValidationStage(internal val label: String) {
    PEM_PARSING("PEM parsing"),
    RSA_VALIDATION("RSA validation"),
    COMPATIBILITY_CHECK("compatibility check"),
}

/**
 * Signing key validation failure. The message reads
 * "<key> validation failed during <stage>: <detail>".
 */
sealed class SigningKeyValidationException(
    detail: String,
    val keyType: KeyType,
    val stage: ValidationStage,
    cause: Throwable? = null,
) : ConfigValidationException("${keyType.label} validation failed during ${stage.label}: $detail", cause)

/**
 * Exception thrown when PEM format validation fails
 */
class InvalidPemFormatException(detail: String, keyType: KeyType, cause: Throwable? = null) :
    SigningKeyValidationException(detail, keyType, ValidationStage.PEM_PARSING, cause)

/**
 * Exception thrown when RSA key validation fails
 */
class InvalidRsaKeyException(detail: String, keyType: KeyType, cause: Throwable? = null) :
    SigningKeyValidationException(detail, keyType, ValidationStage.RSA_VALIDATION, cause)

/**
 * Exception thrown when private and public keys don't match
 */
class KeyMismatchException(detail: String) :
    SigningKeyValidationException(detail, KeyType.BOTH, ValidationStage.COMPATIBILITY_CHECK)
