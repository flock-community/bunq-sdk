package com.bunq.sdk;

import com.bunq.sdk.generated.endpoint.ReadUser;
import community.flock.wirespec.java.Wirespec.RawResponse;
import org.junit.jupiter.api.Test;

import java.nio.charset.StandardCharsets;
import java.util.Map;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class ErrorResponseTest {

    private static ReadUser.Response<?> readUser(int status, String body) {
        return ReadUser.fromRawResponse(Wirespec.serialization,
                new RawResponse(status, Map.of(), Optional.of(body.getBytes(StandardCharsets.UTF_8))));
    }

    @Test
    public void a400ErrorBodyWithoutResponseEnvelopeIsDeserialized() {
        var response = assertInstanceOf(ReadUser.Response400.class,
                readUser(400, "{\"Error\":[{\"error_description\":\"Missing required field \\\"currency\\\".\"}]}"));

        assertEquals("Missing required field \"currency\".",
                response.body().Error().orElseThrow().get(0).error_description().orElseThrow());
    }

    @Test
    public void aStatusOtherThan200And400IsATypedResponse() {
        var response = assertInstanceOf(ReadUser.Response403.class,
                readUser(403, "{\"Error\":[{\"error_description\":\"Insufficient authentication.\"}]}"));

        assertEquals("Insufficient authentication.",
                response.body().Error().orElseThrow().get(0).error_description().orElseThrow());
    }

    @Test
    public void aBodyWithoutResponseOrErrorIsRejected() {
        assertThrows(IllegalStateException.class, () -> readUser(200, "{\"unexpected\":true}"));
    }

    @Test
    public void aNonJsonErrorBodyNamesTheStatus() {
        var html = new RawResponse(500, Map.of(), Optional.of("<html>Internal Server Error</html>".getBytes(StandardCharsets.UTF_8)));

        var e = assertThrows(IllegalStateException.class, () -> Wirespec.failOnNonJsonError(html));

        assertTrue(e.getMessage().contains("500") && e.getMessage().contains("<html>"));
    }
}
