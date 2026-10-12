package com.bunq.sdk;

/**
 * Exception thrown when private and public keys don't match
 */
public final class KeyMismatchException extends SigningKeyValidationException {
    public KeyMismatchException(String detail) {
        super(detail, KeyType.BOTH, ValidationStage.COMPATIBILITY_CHECK, null);
    }
}
