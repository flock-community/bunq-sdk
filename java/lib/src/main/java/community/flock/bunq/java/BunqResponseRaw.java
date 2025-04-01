package community.flock.bunq.java;

import java.util.Map;

public class BunqResponseRaw {

    private final byte[] bodyBytes;
    private final Map<String, String> headers;

    public BunqResponseRaw(byte[] bodyBytes, Map<String, String> headers) {
        this.bodyBytes = bodyBytes;
        this.headers = headers;
    }

    public byte[] getBodyBytes() {
        return bodyBytes;
    }

    public Map<String, String> getHeaders() {
        return headers;
    }
}
