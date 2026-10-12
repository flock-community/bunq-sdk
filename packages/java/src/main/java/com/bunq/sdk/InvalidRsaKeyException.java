package com.bunq.sdk;

/**
 * Exception thrown when RSA key validation fails
 */
public final class InvalidRsaKeyException extends SigningKeyValidationException {
    public InvalidRsaKeyException(String detail, KeyType keyType) {
        this(detail, keyType, null);
    }

    public InvalidRsaKeyException(String detail, KeyType keyType, Throwable cause) {
        super(detail, keyType, ValidationStage.RSA_VALIDATION, cause);
    }
}
