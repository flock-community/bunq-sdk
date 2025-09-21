package com.bunq.sdk;

/**
 * Exception thrown when configuration validation fails
 */
public sealed class ConfigValidationException extends RuntimeException 
    permits InvalidPemFormatException, InvalidRsaKeyException, KeyMismatchException {
    
    public ConfigValidationException(String message) {
        super(message);
    }
    
    public ConfigValidationException(String message, Throwable cause) {
        super(message, cause);
    }
}

/**
 * Exception thrown when PEM format validation fails
 */
final class InvalidPemFormatException extends ConfigValidationException {
    public InvalidPemFormatException(String message) {
        super(message);
    }
    
    public InvalidPemFormatException(String message, Throwable cause) {
        super(message, cause);
    }
}

/**
 * Exception thrown when RSA key validation fails
 */
final class InvalidRsaKeyException extends ConfigValidationException {
    public InvalidRsaKeyException(String message) {
        super(message);
    }
    
    public InvalidRsaKeyException(String message, Throwable cause) {
        super(message, cause);
    }
}

/**
 * Exception thrown when private and public keys don't match
 */
final class KeyMismatchException extends ConfigValidationException {
    public KeyMismatchException(String message) {
        super(message);
    }
}