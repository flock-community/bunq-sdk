/**
 * Configuration for a bunq API server including base URL and pinned key for secure connections
 */
export interface BunqServer {
    readonly baseUrl: string;
    readonly pinnedKey: string;
}

/**
 * Production bunq API server configuration
 */
export const BUNQ_PUBLIC_SERVER: BunqServer = {
    baseUrl: "https://api.bunq.com/v1/",
    pinnedKey: "sha256/nI/T/sDfioCBHB5mVppDPyLi2HXYanwk2arpZuHLOu0="
};

/**
 * Sandbox bunq API server configuration for testing and development
 */
export const BUNQ_SANDBOX_SERVER: BunqServer = {
    baseUrl: "https://public-api.sandbox.bunq.com/v1/",
    pinnedKey: "sha256/++MBgDH5WGvL9Bcn5Be30cRcL0f5O+NyoXuWtQdX1aI="
};