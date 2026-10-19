package com.bunq.sdk;

import com.sun.net.httpserver.HttpExchange;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.security.Signature;
import java.util.Base64;

/** Stands in for bunq's server key: local test servers sign their responses with it. */
final class TestServerKey {
    private static final SigningKeys KEYS = BunqSigningKeysGenerator.generateBunqSigningKeys();
    static final String PUBLIC_PEM = KEYS.publicKeyPem();

    private TestServerKey() {
    }

    static String sign(byte[] body) {
        try {
            Signature signature = Signature.getInstance("SHA256withRSA");
            signature.initSign(KEYS.privateKey());
            signature.update(body);
            return Base64.getEncoder().encodeToString(signature.sign());
        } catch (Exception e) {
            throw new IllegalStateException(e);
        }
    }

    /** Answers with the body and a valid X-Bunq-Server-Signature header. */
    static void respond(HttpExchange exchange, int status, String body) throws IOException {
        respond(exchange, status, body, sign(body.getBytes(StandardCharsets.UTF_8)));
    }

    /** Answers with the body and the given signature header (none when null). */
    static void respond(HttpExchange exchange, int status, String body, String signature) throws IOException {
        byte[] bytes = body.getBytes(StandardCharsets.UTF_8);
        if (signature != null) {
            exchange.getResponseHeaders().add("X-Bunq-Server-Signature", signature);
        }
        exchange.sendResponseHeaders(status, bytes.length == 0 ? -1 : bytes.length);
        if (bytes.length > 0) {
            exchange.getResponseBody().write(bytes);
        }
        exchange.close();
    }
}
