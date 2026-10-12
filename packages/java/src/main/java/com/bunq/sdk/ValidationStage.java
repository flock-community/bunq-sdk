package com.bunq.sdk;

public enum ValidationStage {
    PEM_PARSING("PEM parsing"),
    RSA_VALIDATION("RSA validation"),
    COMPATIBILITY_CHECK("compatibility check");

    final String label;

    ValidationStage(String label) {
        this.label = label;
    }
}
