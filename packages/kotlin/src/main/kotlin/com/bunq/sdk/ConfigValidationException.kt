package com.bunq.sdk

/**
 * Exception thrown when configuration validation fails
 */
sealed class ConfigValidationException(message: String, cause: Throwable? = null) : Exception(message, cause)

/**
 * Exception thrown when PEM format validation fails
 */
class InvalidPemFormatException(message: String, cause: Throwable? = null) : ConfigValidationException(message, cause)

/**
 * Exception thrown when RSA key validation fails
 */
class InvalidRsaKeyException(message: String, cause: Throwable? = null) : ConfigValidationException(message, cause)

/**
 * Exception thrown when private and public keys don't match
 */
class KeyMismatchException(message: String) : ConfigValidationException(message)

