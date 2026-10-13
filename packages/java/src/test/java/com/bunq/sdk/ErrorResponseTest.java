package com.bunq.sdk;

import com.bunq.sdk.generated.endpoint.ReadUser;
import community.flock.wirespec.java.Wirespec.RawResponse;
import org.junit.jupiter.api.Test;

import java.nio.charset.StandardCharsets;
import java.util.Map;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;

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
}
