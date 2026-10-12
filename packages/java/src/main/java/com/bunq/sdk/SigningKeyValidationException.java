package com.bunq.sdk;

/**
 * Signing key validation failure. The message reads
 * "&lt;key&gt; validation failed during &lt;stage&gt;: &lt;detail&gt;".
 */
public sealed class SigningKeyValidationException extends ConfigValidationException
    permits InvalidPemFormatException, InvalidRsaKeyException, KeyMismatchException {

    private final KeyType keyType;
    private final ValidationStage stage;

    SigningKeyValidationException(String detail, KeyType keyType, ValidationStage stage, Throwable cause) {
        super(keyType.label + " validation failed during " + stage.label + ": " + detail, cause);
        this.keyType = keyType;
        this.stage = stage;
    }

    public KeyType keyType() {
        return keyType;
    }

    public ValidationStage stage() {
        return stage;
    }
}
