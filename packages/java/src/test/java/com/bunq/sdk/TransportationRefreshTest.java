package com.bunq.sdk;

import com.sun.net.httpserver.HttpServer;
import community.flock.wirespec.java.Wirespec.RawRequest;
import community.flock.wirespec.java.Wirespec.Transportation;
import org.junit.jupiter.api.Test;

import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.BiConsumer;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class TransportationRefreshTest {

    private static final String AUTHENTICATION_ERROR = "{\"Error\":[{\"error_description\":\"Insufficient authentication.\"}]}";
    private static final RawRequest REQUEST = new RawRequest("GET", List.of("ping"), Map.of(), Map.of(), Optional.empty());

    /** Answers 200 for the token "fresh", otherwise 403 with the given rejection body. */
    private static void withServer(String rejection, BiConsumer<Context, List<String>> block) throws Exception {
        List<String> seenTokens = Collections.synchronizedList(new java.util.ArrayList<>());
        HttpServer server = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
        server.createContext("/", exchange -> {
            String token = exchange.getRequestHeaders().getFirst("X-Bunq-Client-Authentication");
            seenTokens.add(token);
            boolean fresh = "fresh".equals(token);
            byte[] body = (fresh ? "{}" : rejection).getBytes(StandardCharsets.UTF_8);
            exchange.sendResponseHeaders(fresh ? 200 : 403, body.length == 0 ? -1 : body.length);
            if (body.length > 0) {
                exchange.getResponseBody().write(body);
            }
            exchange.close();
        });
        server.start();
        try {
            Config config = new Config(
                    new BunqServer("http://127.0.0.1:" + server.getAddress().getPort() + "/", ""),
                    "test", "key", BunqSigningKeysGenerator.generateBunqSigningKeys(),
                    null, null, null, null, null, null);
            block.accept(new Context("", 1, 1, "stale", 1, Instant.now(), "installation", config), seenTokens);
        } finally {
            server.stop(0);
        }
    }

    private static Context fresh(Context context) {
        return new Context(context.serverPublicKey(), context.deviceId(), context.sessionId(), "fresh", context.userId(),
                context.sessionExpiryTime(), context.installationToken(), context.config());
    }

    @Test
    public void insufficientAuthenticationRefreshesOnceAndRetriesWithTheNewToken() throws Exception {
        withServer(AUTHENTICATION_ERROR, (context, tokens) -> {
            var refreshes = new AtomicInteger();
            Transportation transport = Wirespec.transportation(context, c -> {
                refreshes.incrementAndGet();
                return fresh(c);
            });

            assertEquals(200, transport.transport(REQUEST).join().statusCode());
            assertEquals(1, refreshes.get());
            assertEquals(List.of("stale", "fresh"), tokens);
        });
    }

    @Test
    public void aFailingRefreshReturnsTheOriginal403() throws Exception {
        withServer(AUTHENTICATION_ERROR, (context, tokens) -> {
            Transportation transport = Wirespec.transportation(context, c -> {
                throw new IllegalStateException("429");
            });

            assertEquals(403, transport.transport(REQUEST).join().statusCode());
            assertEquals(List.of("stale"), tokens);
        });
    }

    @Test
    public void another403DoesNotRefresh() throws Exception {
        withServer("{\"Error\":[{\"error_description\":\"You are not allowed to make this call.\"}]}", (context, tokens) -> {
            var refreshes = new AtomicInteger();
            Transportation transport = Wirespec.transportation(context, c -> {
                refreshes.incrementAndGet();
                return fresh(c);
            });

            assertEquals(403, transport.transport(REQUEST).join().statusCode());
            assertEquals(0, refreshes.get());
        });
    }

    @Test
    public void a403WithANonJsonOrEmptyBodyDoesNotRefresh() throws Exception {
        for (String rejection : List.of("<html>forbidden</html>", "")) {
            withServer(rejection, (context, tokens) -> {
                var refreshes = new AtomicInteger();
                Transportation transport = Wirespec.transportation(context, c -> {
                    refreshes.incrementAndGet();
                    return fresh(c);
                });

                assertEquals(403, transport.transport(REQUEST).join().statusCode());
                assertEquals(0, refreshes.get());
            });
        }
    }

    @Test
    public void concurrentCallsRefreshOnce() throws Exception {
        withServer(AUTHENTICATION_ERROR, (context, tokens) -> {
            var refreshes = new AtomicInteger();
            Transportation transport = Wirespec.transportation(context, c -> {
                try {
                    Thread.sleep(200);
                } catch (InterruptedException e) {
                    throw new IllegalStateException(e);
                }
                refreshes.incrementAndGet();
                return fresh(c);
            });

            var first = transport.transport(REQUEST);
            var second = transport.transport(REQUEST);
            CompletableFuture.allOf(first, second).join();

            assertEquals(200, first.join().statusCode());
            assertEquals(200, second.join().statusCode());
            assertEquals(1, refreshes.get());
        });
    }
}
