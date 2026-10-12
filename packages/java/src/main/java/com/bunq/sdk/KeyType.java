package com.bunq.sdk;

public enum KeyType {
    PRIVATE("Private key"),
    PUBLIC("Public key"),
    BOTH("Private and public key");

    final String label;

    KeyType(String label) {
        this.label = label;
    }
}
