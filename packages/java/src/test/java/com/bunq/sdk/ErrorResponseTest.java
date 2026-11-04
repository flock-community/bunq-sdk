package com.bunq.sdk;

import com.bunq.sdk.generated.endpoint.ReadUser;
import com.sun.net.httpserver.HttpServer;
import community.flock.wirespec.java.Wirespec.RawResponse;
import org.junit.jupiter.api.Test;

import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.CompletionException;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class ErrorResponseTest {

    private static ReadUser.Response<?> readUser(int status, String body) {
        return ReadUser.fromRawResponse(Wirespec.serialization,
                new RawResponse(status, Map.of(), Optional.of(body.getBytes(StandardCharsets.UTF_8))));
    }

    private static ReadUser.Response<?> readUserFrom(int status, String body) throws Exception {
        return readUserFrom(status, body, Map.of());
    }

    private static ReadUser.Response<?> readUserFrom(int status, String body, Map<String, String> headers) throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
        server.createContext("/", exchange -> {
            headers.forEach((name, value) -> exchange.getResponseHeaders().add(name, value));
            TestServerKey.respond(exchange, status, body);
        });
        server.start();
        try {
            Config config = new Config(
                    new BunqServer("http://127.0.0.1:" + server.getAddress().getPort() + "/", ""),
                    "test", "key", BunqSigningKeysGenerator.generateBunqSigningKeys(),
                    null, null, null, null, null, null);
            var context = new Context(TestServerKey.PUBLIC_PEM, 1, 1, "token", 1, Instant.now().plusSeconds(3600), "installation", config);
            return Wirespec.bunqClient(context).readUser(1L).join();
        } finally {
            server.stop(0);
        }
    }

    private static BunqApiException failureFrom(int status, String body) {
        var e = assertThrows(CompletionException.class, () -> readUserFrom(status, body));
        return assertInstanceOf(BunqApiException.class, e.getCause());
    }

    @Test
    public void a400ErrorBodyWithoutResponseEnvelopeIsATypedResponse400() throws Exception {
        var response = assertInstanceOf(ReadUser.Response400.class,
                readUserFrom(400, "{\"Error\":[{\"error_description\":\"Missing required field \\\"currency\\\".\"}]}"));

        assertEquals("Missing required field \"currency\".",
                response.body().Error().orElseThrow().get(0).error_description().orElseThrow());
    }

    @Test
    public void aBodyWithoutResponseOrErrorIsRejected() {
        assertThrows(IllegalStateException.class, () -> readUser(200, "{\"unexpected\":true}"));
    }

    @Test
    public void aStatusOtherThan200And400ThrowsWithTheStatusAndBody() {
        for (int status : new int[]{403, 404, 500}) {
            var body = "{\"Error\":[{\"error_description\":\"nope " + status + "\"}]}";

            var e = failureFrom(status, body);

            assertEquals(status, e.status());
            assertEquals(body, e.body());
        }
    }

    @Test
    public void anHtml500ThrowsWithTheHtmlAsBody() {
        var e = failureFrom(500, "<html>Internal Server Error</html>");

        assertEquals(500, e.status());
        assertEquals("<html>Internal Server Error</html>", e.body());
    }

    @Test
    public void a400ThatIsNotJsonThrows() {
        assertEquals(400, failureFrom(400, "<html>Bad Request</html>").status());
    }

    @Test
    public void a200WithoutResponseThrowsWithTheStatusAndBody() {
        var e = failureFrom(200, "{\"unexpected\":true}");

        assertEquals(200, e.status());
        assertEquals("{\"unexpected\":true}", e.body());
    }

    @Test
    public void a400WithoutErrorThrowsWithTheStatusAndBody() {
        var e = failureFrom(400, "{\"message\":\"Bad Request\"}");

        assertEquals(400, e.status());
        assertEquals("{\"message\":\"Bad Request\"}", e.body());
    }

    @Test
    public void aNonObjectJson200Throws() {
        var e = failureFrom(200, "[]");

        assertEquals(200, e.status());
        assertEquals("[]", e.body());
    }

    @Test
    public void theExceptionCarriesTheResponseHeadersButTheMessageDoesNot() {
        var e = assertInstanceOf(BunqApiException.class, assertThrows(CompletionException.class, () -> readUserFrom(
                429, "{\"Error\":[{\"error_description\":\"Too many requests.\"}]}",
                Map.of("X-Bunq-Client-Response-Id", "response-id-123", "Retry-After", "30"))).getCause());

        assertEquals(List.of("response-id-123"), header(e, "X-Bunq-Client-Response-Id"));
        assertEquals(List.of("30"), header(e, "Retry-After"));
        assertFalse(e.getMessage().contains("response-id-123"));
    }

    private static List<String> header(BunqApiException e, String name) {
        return e.headers().entrySet().stream()
                .filter(h -> h.getKey() != null && h.getKey().equalsIgnoreCase(name))
                .findFirst().orElseThrow().getValue();
    }

    @Test
    public void theMessageTruncatesTheBodyButTheBodyFieldKeepsItWhole() {
        var e = new BunqApiException(502, "x".repeat(2000));

        assertTrue(e.getMessage().length() < 600);
        assertEquals(2000, e.body().length());
    }

    @Test
    public void a200IsReturnedAsIs() throws Exception {
        assertInstanceOf(ReadUser.Response200.class, readUserFrom(200, "{\"Response\":[{\"UserPerson\":{\"id\":1}}]}"));
    }
}
