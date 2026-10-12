package com.bunq.sdk;

/**
 * Exception thrown when configuration validation fails
 */
public sealed class ConfigValidationException extends RuntimeException
    permits SigningKeyValidationException {

    public ConfigValidationException(String message) {
        super(message);
    }

    public ConfigValidationException(String message, Throwable cause) {
        super(message, cause);
    }
}
