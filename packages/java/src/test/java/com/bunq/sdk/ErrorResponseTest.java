package com.bunq.sdk;

import com.bunq.sdk.generated.endpoint.ReadUser;
import com.sun.net.httpserver.HttpServer;
import community.flock.wirespec.java.Wirespec.RawResponse;
import org.junit.jupiter.api.Test;

import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.CompletionException;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class ErrorResponseTest {

    private static ReadUser.Response<?> readUser(int status, String body) {
        return ReadUser.fromRawResponse(Wirespec.serialization,
                new RawResponse(status, Map.of(), Optional.of(body.getBytes(StandardCharsets.UTF_8))));
    }

    private static ReadUser.Response<?> readUserFrom(int status, String body) throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
        server.createContext("/", exchange -> {
            byte[] bytes = body.getBytes(StandardCharsets.UTF_8);
            exchange.sendResponseHeaders(status, bytes.length);
            exchange.getResponseBody().write(bytes);
            exchange.close();
        });
        server.start();
        try {
            Config config = new Config(
                    new BunqServer("http://127.0.0.1:" + server.getAddress().getPort() + "/", ""),
                    "test", "key", BunqSigningKeysGenerator.generateBunqSigningKeys(),
                    null, null, null, null, null, null);
            var context = new Context("", 1, 1, "token", 1, Instant.now(), "installation", config);
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
