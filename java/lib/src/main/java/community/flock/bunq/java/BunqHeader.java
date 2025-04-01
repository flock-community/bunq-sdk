package community.flock.bunq.java;

import com.bunq.sdk.http.BunqRequestBuilder;
import community.flock.wirespec.java.Wirespec;

import java.util.Collection;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

public enum BunqHeader {
    ATTACHMENT_DESCRIPTION("X-Bunq-Attachment-Description"),
    CACHE_CONTROL("Cache-Control", "no-cache"),
    CLIENT_AUTHENTICATION("X-Bunq-Client-Authentication"),
    CLIENT_ENCRYPTION_HMAC("X-Bunq-Client-Encryption-Hmac"),
    CLIENT_ENCRYPTION_IV("X-Bunq-Client-Encryption-Iv"),
    CLIENT_ENCRYPTION_KEY("X-Bunq-Client-Encryption-Key"),
    CLIENT_REQUEST_ID("X-Bunq-Client-Request-Id"),
    CLIENT_RESPONSE_ID("X-Bunq-Client-Response-Id", "Could not determine response id."),
    CLIENT_SIGNATURE("X-Bunq-Client-Signature"),
    CONTENT_TYPE("Content-Type"),
    GEOLOCATION("X-Bunq-Geolocation", "0 0 0 0 000"),
    LANGUAGE("X-Bunq-Language", "en_US"),
    REGION("X-Bunq-Region", "nl_NL"),
    SERVER_SIGNATURE("X-Bunq-Server-Signature"),
    USER_AGENT("User-Agent", "bunq-sdk-java/1.14.18");

    private static final String PREFIX = "X-Bunq-";

    private final String header;
    private final String defaultValue;

    BunqHeader(String header) {
        this(header, null);
    }

    BunqHeader(String header, String defaultValue) {
        this.header = header;
        this.defaultValue = defaultValue;
    }

    public static BunqHeader parseHeaderOrNull(String value) {
        for (BunqHeader header : values()) {
            if (header.equals(value)) {
                return header;
            }
        }

        return null;
    }

    public String getHeaderName() {
        return header;
    }

    public String getDefaultValue() {
        return defaultValue;
    }

    public Map.Entry<String, String> getHeaderEntryOrDefault(String value) {
        return new java.util.AbstractMap.SimpleEntry<>(getHeaderName(), getHeaderValueOrDefault(value));
    }
    public String getHeaderValueOrDefault(String value) {
        if (value != null) {
            return value;
        }

        return getDefaultValue();
    }

    public void addTo(Map<String, String> headers, String value) {
        headers.put(getHeaderName(), getHeaderValueOrDefault(value));
    }

    public void addTo(BunqRequestBuilder requestBuilder) {
        addTo(requestBuilder, null);
    }

    public void addTo(BunqRequestBuilder requestBuilder, String value) {
        requestBuilder.addHeader(getHeaderName(), getHeaderValueOrDefault(value));
    }

    public boolean equals(String header) {
        return getHeaderName().equalsIgnoreCase(header);
    }

    public boolean isBunq() {
        return getHeaderName().startsWith(PREFIX);
    }

    private String findKeyOrNull(Collection<String> keys) {
        for (String key : keys) {
            if (this.equals(key)) {
                return key;
            }
        }

        return null;
    }

    public String getHeaderValueOrDefault(Map<String, String> headers) {
        String key = findKeyOrNull(headers.keySet());

        if (key != null && headers.get(key) != null) {
            return headers.get(key);
        }

        return getDefaultValue();
    }


    /**
     * Combines two maps into a new map. If there are duplicate keys, values from the second map will override the first.
     */
    public static Map<String, String> mergeMaps(Map<String, String> map1, Map<String, String> map2) {
        return new HashMap<>() {{
            putAll(map1);
            putAll(map2);
        }};
    }

    public static Map<String, String> bunqHeaders(Wirespec.Method method, String body, Context context) {
        return mergeMaps(defaultHeaders(), sessionHeaders(method, body, context));
    }

    public static Map<String, String> defaultHeaders() {
        HashMap<String, String> map = new HashMap<>();
        BunqHeader.CACHE_CONTROL.addTo(map, null);
        BunqHeader.USER_AGENT.addTo(map, null);
        BunqHeader.LANGUAGE.addTo(map, null);
        BunqHeader.REGION.addTo(map, null);
        BunqHeader.CLIENT_REQUEST_ID.addTo(map, UUID.randomUUID().toString());
        BunqHeader.GEOLOCATION.addTo(map, null);
        return map;
    }

    private static Map<String, String> sessionHeaders(Wirespec.Method method, String body, Context context) {
        var map = new HashMap<String, String>();
        BunqHeader.CLIENT_AUTHENTICATION.addTo(map, context.sessionToken());
        BunqHeader.CLIENT_SIGNATURE.addTo(map, SecurityUtils.generateSignature(method, body, context.keyPair()));
        return map;
    }

}
