package com.bunq.sdk;

/** bunq (or a proxy in front of it) answered with a status other than 200 or 400, or with a 400 that is not JSON. */
public class BunqApiException extends RuntimeException {
    private static final int MAX_MESSAGE_BODY = 500;

    private final int status;
    private final String body;

    public BunqApiException(int status, String body) {
        super("bunq answered " + status + ": " + body.substring(0, Math.min(body.length(), MAX_MESSAGE_BODY)));
        this.status = status;
        this.body = body;
    }

    public int status() {
        return status;
    }

    public String body() {
        return body;
    }
}
