package com.bunq.sdk;

import com.bunq.sdk.generated.Client;
import com.bunq.sdk.generated.endpoint.DeleteSession;
import com.bunq.sdk.generated.endpoint.ListAllMonetaryAccountBankForUser;
import com.fasterxml.jackson.databind.JsonNode;
import org.junit.jupiter.api.Test;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.Optional;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;

/** Runs against the bunq sandbox with a freshly created sandbox user. */
public class DeadSessionTest {

    static String newSandboxApiKey() throws Exception {
        HttpRequest request = HttpRequest.newBuilder(URI.create(BunqServer.BUNQ_SANDBOX_SERVER.baseUrl() + "sandbox-user-person"))
                .header("User-Agent", "DeadSessionTest")
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString("{}"))
                .build();
        HttpResponse<String> response = HttpClient.newHttpClient().send(request, HttpResponse.BodyHandlers.ofString());
        assertEquals(200, response.statusCode());
        for (JsonNode item : Wirespec.objectMapper.readTree(response.body()).get("Response")) {
            if (item.has("ApiKey")) {
                return item.get("ApiKey").get("api_key").asText();
            }
        }
        throw new IllegalStateException("No api key in sandbox user response");
    }

    @Test
    public void aDeadSessionIsRefreshedOnceAndTheCallSucceeds() throws Exception {
        Config config = new Config(BunqServer.BUNQ_SANDBOX_SERVER, "DeadSessionTest", newSandboxApiKey(),
                BunqSigningKeysGenerator.generateBunqSigningKeys(), null, null, null, null, null, null);
        Context context = Context.initContext(config);
        var refreshes = new AtomicInteger();
        Client client = new Client(Wirespec.serialization, Wirespec.refreshingTransportation(context, c -> {
            refreshes.incrementAndGet();
            return c.refreshSession();
        }));

        assertInstanceOf(ListAllMonetaryAccountBankForUser.Response200.class,
                client.listAllMonetaryAccountBankForUser(context.userId(), Optional.empty(), Optional.empty(), Optional.empty()).get());
        assertEquals(0, refreshes.get());

        assertInstanceOf(DeleteSession.Response200.class, client.deleteSession(context.sessionId()).get());

        assertInstanceOf(ListAllMonetaryAccountBankForUser.Response200.class,
                client.listAllMonetaryAccountBankForUser(context.userId(), Optional.empty(), Optional.empty(), Optional.empty()).get());
        assertEquals(1, refreshes.get());
    }
}
