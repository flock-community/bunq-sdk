package com.bunq.sdk;

import com.sun.net.httpserver.HttpServer;
import community.flock.wirespec.java.Wirespec.RawRequest;
import org.junit.jupiter.api.Test;

import java.net.InetSocketAddress;
import java.net.http.HttpTimeoutException;
import java.time.Duration;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.CompletionException;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicReference;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;

public class SendTest {

    private static Config config(int port, Duration connectTimeout, Duration requestTimeout) {
        return new Config(
                new BunqServer("http://127.0.0.1:" + port + "/", ""),
                "test", "key", BunqSigningKeysGenerator.generateBunqSigningKeys(),
                null, null, null, null, null, null, connectTimeout, requestTimeout);
    }

    private static RawRequest get(Map<String, List<String>> queries) {
        return new RawRequest("GET", List.of("payment"), queries, Map.of(), Optional.empty());
    }

    private static String receivedQuery(Map<String, List<String>> queries) throws Exception {
        var query = new AtomicReference<String>();
        HttpServer server = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
        server.createContext("/", exchange -> {
            query.set(exchange.getRequestURI().getRawQuery());
            exchange.sendResponseHeaders(200, -1);
            exchange.close();
        });
        server.start();
        try {
            Wirespec.send(config(server.getAddress().getPort(), null, null), get(queries)).join();
        } finally {
            server.stop(0);
        }
        return query.get();
    }

    @Test
    public void queryParametersWithoutAValueAreLeftOut() throws Exception {
        assertEquals("count=200", receivedQuery(Map.of("count", List.of("200"), "newer_id", List.of(), "older_id", List.of())));
    }

    @Test
    public void noQueryStringIsSentWhenNoParameterHasAValue() throws Exception {
        assertNull(receivedQuery(Map.of("newer_id", List.of(), "older_id", List.of())));
    }

    @Test
    public void aRequestWithoutAnAnswerWithinTheRequestTimeoutFailsWithHttpTimeoutException() throws Exception {
        var release = new CountDownLatch(1);
        HttpServer server = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
        server.createContext("/", exchange -> {
            try {
                release.await(10, TimeUnit.SECONDS);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            exchange.close();
        });
        server.start();
        try {
            var config = config(server.getAddress().getPort(), null, Duration.ofMillis(200));

            var e = assertThrows(CompletionException.class, () -> Wirespec.send(config, get(Map.of())).join());

            assertInstanceOf(HttpTimeoutException.class, e.getCause());
        } finally {
            release.countDown();
            server.stop(0);
        }
    }

    @Test
    public void theConnectTimeoutIsSetOnTheHttpClient() {
        var timeout = Duration.ofSeconds(3);

        assertEquals(Optional.of(timeout), Wirespec.httpClientFor(config(1, timeout, null)).connectTimeout());
        assertEquals(Optional.empty(), Wirespec.httpClientFor(config(1, null, null)).connectTimeout());
    }
}
