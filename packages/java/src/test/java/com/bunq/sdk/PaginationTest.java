package com.bunq.sdk;

import com.bunq.sdk.generated.endpoint.ListAllMonetaryAccountBankForUser;
import com.sun.net.httpserver.HttpServer;
import org.junit.jupiter.api.Test;

import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class PaginationTest {

    private static ListAllMonetaryAccountBankForUser.Response<?> listFrom(String body) throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
        server.createContext("/", exchange -> {
            byte[] bytes = body.getBytes(StandardCharsets.UTF_8);
            exchange.sendResponseHeaders(200, bytes.length);
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
            return Wirespec.bunqClient(context)
                    .listAllMonetaryAccountBankForUser(1L, Optional.of(2L), Optional.empty(), Optional.empty()).join();
        } finally {
            server.stop(0);
        }
    }

    @Test
    public void aListResponseKeepsTheItemsAndThePaginationBlock() throws Exception {
        var response = assertInstanceOf(ListAllMonetaryAccountBankForUser.Response200.class, listFrom("""
                {"Response":[{"MonetaryAccountBank":{"id":2,"description":"second"}},{"MonetaryAccountBank":{"id":1,"description":"first"}}],
                 "Pagination":{"future_url":"/v1/future?newer_id=2","newer_url":null,"older_url":"/v1/older?older_id=1"}}
                """));

        var page = response.body();
        assertEquals(List.of(2L, 1L), page.Response().stream().map(item -> item.id().orElseThrow()).toList());
        assertEquals("/v1/future?newer_id=2", page.Pagination().future_url().orElseThrow());
        assertTrue(page.Pagination().newer_url().isEmpty());
        assertEquals("/v1/older?older_id=1", page.Pagination().older_url().orElseThrow());
    }

    @Test
    public void anEmptyPageHasAnEmptyListAndItsPagination() throws Exception {
        var response = assertInstanceOf(ListAllMonetaryAccountBankForUser.Response200.class, listFrom(
                "{\"Response\":[],\"Pagination\":{\"future_url\":null,\"newer_url\":null,\"older_url\":null}}"));

        assertTrue(response.body().Response().isEmpty());
        assertTrue(response.body().Pagination().older_url().isEmpty());
    }
}
