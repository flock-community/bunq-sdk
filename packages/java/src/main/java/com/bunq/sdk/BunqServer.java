package com.bunq.sdk;

/**
 * Configuration for a bunq API server, including the base URL and SSL pinned key.
 */
public record BunqServer(String baseUrl, String pinnedKey) {
    
    /**
     * Production bunq server configuration
     */
    public static final BunqServer BUNQ_PUBLIC_SERVER = new BunqServer(
        "https://api.bunq.com/v1/",
        "sha256/nI/T/sDfioCBHB5mVppDPyLi2HXYanwk2arpZuHLOu0="
    );
    
    /**
     * Sandbox bunq server configuration for testing
     */
    public static final BunqServer BUNQ_SANDBOX_SERVER = new BunqServer(
        "https://public-api.sandbox.bunq.com/v1/",
        "sha256/++MBgDH5WGvL9Bcn5Be30cRcL0f5O+NyoXuWtQdX1aI="
    );
}