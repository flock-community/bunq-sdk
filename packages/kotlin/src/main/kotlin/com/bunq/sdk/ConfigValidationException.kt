package com.bunq.sdk

/**
 * Exception thrown when configuration validation fails
 */
sealed class ConfigValidationException(message: String, cause: Throwable? = null) : Exception(message, cause)

enum class KeyType { PRIVATE, PUBLIC, BOTH }

enum class ValidationStage { PEM_PARSING, RSA_VALIDATION, COMPATIBILITY_CHECK }

/**
 * Signing key validation failure, reporting which key failed and at which stage.
 */
sealed class SigningKeyValidationException(
    message: String,
    val keyType: KeyType,
    val stage: ValidationStage,
    cause: Throwable? = null,
) : ConfigValidationException(message, cause)

/**
 * Exception thrown when PEM format validation fails
 */
class InvalidPemFormatException(
    message: String,
    keyType: KeyType,
    stage: ValidationStage = ValidationStage.PEM_PARSING,
    cause: Throwable? = null,
) : SigningKeyValidationException(message, keyType, stage, cause)

/**
 * Exception thrown when RSA key validation fails
 */
class InvalidRsaKeyException(
    message: String,
    keyType: KeyType,
    stage: ValidationStage = ValidationStage.RSA_VALIDATION,
    cause: Throwable? = null,
) : SigningKeyValidationException(message, keyType, stage, cause)

/**
 * Exception thrown when private and public keys don't match
 */
class KeyMismatchException(
    message: String,
    keyType: KeyType = KeyType.BOTH,
    stage: ValidationStage = ValidationStage.COMPATIBILITY_CHECK,
) : SigningKeyValidationException(message, keyType, stage)
