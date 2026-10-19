package com.bunq.sdk;

import com.sun.net.httpserver.HttpServer;
import community.flock.wirespec.java.Wirespec.RawRequest;
import community.flock.wirespec.java.Wirespec.RawResponse;
import org.junit.jupiter.api.Test;

import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.CompletionException;
import java.util.concurrent.ExecutionException;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class ResponseSignatureTest {

    private static final String BODY = "{\"Response\":[]}";
    private static final RawRequest REQUEST = new RawRequest("GET", List.of("ping"), Map.of(), Map.of(), Optional.empty());

    private static byte[] bytes(String s) {
        return s.getBytes(StandardCharsets.UTF_8);
    }

    private static RawResponse call(int status, String body, String signature) throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
        server.createContext("/", exchange -> TestServerKey.respond(exchange, status, body, signature));
        server.start();
        try {
            Config config = new Config(
                    new BunqServer("http://127.0.0.1:" + server.getAddress().getPort() + "/", ""),
                    "test", "key", BunqSigningKeysGenerator.generateBunqSigningKeys(),
                    null, null, null, null, null, null);
            var context = new Context(TestServerKey.PUBLIC_PEM, 1, 1, "token", 1, Instant.now().plusSeconds(3600), "installation", config);
            return Wirespec.transportation(context, c -> { }).transport(REQUEST).join();
        } finally {
            server.stop(0);
        }
    }

    private static void assertRejected(String signature) {
        assertRejected(200, BODY, signature);
    }

    private static void assertRejected(int status, String body, String signature) {
        var e = assertThrows(CompletionException.class, () -> call(status, body, signature));
        assertEquals("Invalid bunq server signature", assertInstanceOf(SecurityException.class, e.getCause()).getMessage());
    }

    @Test
    public void aValidSignaturePasses() throws Exception {
        assertEquals(200, call(200, BODY, TestServerKey.sign(bytes(BODY))).statusCode());
    }

    @Test
    public void aValidSignatureOnA400Passes() throws Exception {
        String error = "{\"Error\":[{\"error_description\":\"x\"}]}";
        assertEquals(400, call(400, error, TestServerKey.sign(bytes(error))).statusCode());
    }

    @Test
    public void aFourHundredWithAnInvalidSignatureThrows() {
        assertRejected(400, "{\"Error\":[{\"error_description\":\"x\"}]}", TestServerKey.sign(bytes("other")));
    }

    @Test
    public void aFourHundredWithAMissingSignatureThrows() {
        assertRejected(400, "{\"Error\":[{\"error_description\":\"x\"}]}", null);
    }

    @Test
    public void initContextThrowsOnAnUnsignedDeviceServerResponse() throws Exception {
        String installation = "{\"Response\":[{\"Id\":{\"id\":1}},{\"Token\":{\"token\":\"t\"}},{\"ServerPublicKey\":{\"server_public_key\":\""
                + TestServerKey.PUBLIC_PEM.replace("\n", "\\n") + "\"}}]}";
        HttpServer server = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
        server.createContext("/", exchange -> TestServerKey.respond(exchange, 200,
                exchange.getRequestURI().getPath().endsWith("installation") ? installation : "{\"Response\":[{\"Id\":{\"id\":3}}]}", null));
        server.start();
        try {
            Config config = new Config(
                    new BunqServer("http://127.0.0.1:" + server.getAddress().getPort() + "/", ""),
                    "test", "key", BunqSigningKeysGenerator.generateBunqSigningKeys(),
                    null, null, null, null, null, null);
            var e = assertThrows(RuntimeException.class, () -> Context.initContext(config));
            var cause = assertInstanceOf(ExecutionException.class, e.getCause()).getCause();
            assertEquals("Invalid bunq server signature", assertInstanceOf(SecurityException.class, cause).getMessage());
        } finally {
            server.stop(0);
        }
    }

    @Test
    public void aSignatureOverAnotherBodyThrows() {
        assertRejected(TestServerKey.sign(bytes("other")));
    }

    @Test
    public void aMissingSignatureThrows() {
        assertRejected(null);
    }

    @Test
    public void aSignatureThatIsNotBase64Throws() {
        assertRejected("not base64!");
    }

    @Test
    public void verifyResponseChecksTheRawBodyBytes() {
        byte[] body = bytes("{\"a\": 1}\n");
        String signature = TestServerKey.sign(body);
        assertTrue(Signing.verifyResponse(TestServerKey.PUBLIC_PEM, body, signature));
        assertFalse(Signing.verifyResponse(TestServerKey.PUBLIC_PEM, bytes("{\"a\":1}"), signature));
    }
}
