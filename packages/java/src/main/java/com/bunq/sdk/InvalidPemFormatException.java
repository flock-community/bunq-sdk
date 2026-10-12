package com.bunq.sdk;

/**
 * Exception thrown when PEM format validation fails
 */
public final class InvalidPemFormatException extends SigningKeyValidationException {
    public InvalidPemFormatException(String detail, KeyType keyType) {
        this(detail, keyType, null);
    }

    public InvalidPemFormatException(String detail, KeyType keyType, Throwable cause) {
        super(detail, keyType, ValidationStage.PEM_PARSING, cause);
    }
}
