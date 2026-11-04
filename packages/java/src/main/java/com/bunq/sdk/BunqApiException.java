package com.bunq.sdk;

import java.util.List;
import java.util.Map;

/**
 * bunq (or a proxy in front of it) answered with a status other than 200 or 400, or with a 400 that is not JSON.
 * {@link #headers()} are the response headers (for example {@code X-Bunq-Client-Response-Id}); they are left out of the message, which ends up in logs.
 */
public class BunqApiException extends RuntimeException {
    private static final int MAX_MESSAGE_BODY = 500;

    private final int status;
    private final String body;
    private final Map<String, List<String>> headers;

    public BunqApiException(int status, String body) {
        this(status, body, Map.of());
    }

    public BunqApiException(int status, String body, Map<String, List<String>> headers) {
        super("Received " + status + ": " + body.substring(0, Math.min(body.length(), MAX_MESSAGE_BODY)));
        this.status = status;
        this.body = body;
        this.headers = headers;
    }

    public int status() {
        return status;
    }

    public String body() {
        return body;
    }

    public Map<String, List<String>> headers() {
        return headers;
    }
}
