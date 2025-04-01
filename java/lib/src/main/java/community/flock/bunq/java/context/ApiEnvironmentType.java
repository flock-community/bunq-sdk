package community.flock.bunq.java.context;

/**
 * Enum for the API environment types and their URIs.
 */
public enum ApiEnvironmentType {

    PRODUCTION(
            "api.bunq.com",
            "v1",
            "sha256/nI/T/sDfioCBHB5mVppDPyLi2HXYanwk2arpZuHLOu0="
    ),
    SANDBOX(
            "public-api.sandbox.bunq.com",
            "v1",
            "sha256/++MBgDH5WGvL9Bcn5Be30cRcL0f5O+NyoXuWtQdX1aI="
    );

    /**
     * Base URI of each given environment.
     */
    private final String baseUri;
    private final String apiVersion;
    private final String pinnedKey;

    ApiEnvironmentType(String baseUri, String apiVersion, String pinnedKey) {
        this.baseUri = baseUri;
        this.apiVersion = apiVersion;
        this.pinnedKey = pinnedKey;
    }

    /**
     * @return Base URI of the environment.
     */
    public String getBaseUri() {
        return this.baseUri;
    }

    public String getApiVersion() {
        return this.apiVersion;
    }

    public String getPinnedKey() {
        return pinnedKey;
    }
}
