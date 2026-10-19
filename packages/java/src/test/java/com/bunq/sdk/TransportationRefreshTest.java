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
import java.util.concurrent.CompletionException;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.BiConsumer;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertThrows;

public class TransportationRefreshTest {

    private static final String AUTHENTICATION_ERROR = "{\"Error\":[{\"error_description\":\"Insufficient authentication.\"}]}";
    private static final RawRequest REQUEST = new RawRequest("GET", List.of("ping"), Map.of(), Map.of(), Optional.empty());

    /** Set by {@link #fresh}: like bunq, the server accepts the session again after a refresh although the token stays the same. */
    private static final AtomicBoolean REVIVED = new AtomicBoolean();

    /** Answers 200 once revived, otherwise 403 with the given rejection body. */
    private static void withServer(String rejection, BiConsumer<Context, List<String>> block) throws Exception {
        withServer(rejection, Instant.now().plusSeconds(3600), block);
    }

    private static void withServer(String rejection, Instant expiry, BiConsumer<Context, List<String>> block) throws Exception {
        REVIVED.set(false);
        List<String> seenTokens = Collections.synchronizedList(new java.util.ArrayList<>());
        HttpServer server = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
        server.createContext("/", exchange -> {
            String token = exchange.getRequestHeaders().getFirst("X-Bunq-Client-Authentication");
            seenTokens.add(token);
            boolean fresh = REVIVED.get();
            byte[] body = (fresh ? "{\"Response\":[]}" : rejection).getBytes(StandardCharsets.UTF_8);
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
            block.accept(new Context("", 1, 1, "stale", 1, expiry, "installation", config), seenTokens);
        } finally {
            server.stop(0);
        }
    }

    private static BunqApiException failure(Transportation transport) {
        var e = assertThrows(CompletionException.class, () -> transport.transport(REQUEST).join());
        return assertInstanceOf(BunqApiException.class, e.getCause());
    }

    /** What bunq returns for a re-created session: the same token with a later expiry. */
    private static Context fresh(Context context) {
        REVIVED.set(true);
        return new Context(context.serverPublicKey(), context.deviceId(), context.sessionId(), context.sessionToken(), context.userId(),
                Instant.now().plusSeconds(3600), context.installationToken(), context.config());
    }

    @Test
    public void insufficientAuthenticationRefreshesOnceAndRetriesWithTheNewToken() throws Exception {
        withServer(AUTHENTICATION_ERROR, (context, tokens) -> {
            var refreshes = new AtomicInteger();
            Transportation transport = Wirespec.refreshingTransportation(context, c -> {
                refreshes.incrementAndGet();
                return fresh(c);
            });

            assertEquals(200, transport.transport(REQUEST).join().statusCode());
            assertEquals(1, refreshes.get());
            assertEquals(List.of("stale", "stale"), tokens);
        });
    }

    @Test
    public void aFailingRefreshThrowsTheOriginal403() throws Exception {
        withServer(AUTHENTICATION_ERROR, (context, tokens) -> {
            Transportation transport = Wirespec.refreshingTransportation(context, c -> {
                throw new IllegalStateException("429");
            });

            var e = failure(transport);

            assertEquals(403, e.status());
            assertEquals(AUTHENTICATION_ERROR, e.body());
            assertEquals(List.of("stale"), tokens);
        });
    }

    @Test
    public void another403DoesNotRefresh() throws Exception {
        withServer("{\"Error\":[{\"error_description\":\"You are not allowed to make this call.\"}]}", (context, tokens) -> {
            var refreshes = new AtomicInteger();
            Transportation transport = Wirespec.refreshingTransportation(context, c -> {
                refreshes.incrementAndGet();
                return fresh(c);
            });

            assertEquals(403, failure(transport).status());
            assertEquals(0, refreshes.get());
        });
    }

    @Test
    public void a403WithAnEmptyBodyDoesNotRefresh() throws Exception {
        withServer("", (context, tokens) -> {
            var refreshes = new AtomicInteger();
            Transportation transport = Wirespec.refreshingTransportation(context, c -> {
                refreshes.incrementAndGet();
                return fresh(c);
            });

            assertEquals(403, failure(transport).status());
            assertEquals(0, refreshes.get());
        });
    }

    @Test
    public void a403WithAnHtmlBodyThrowsAndDoesNotRefresh() throws Exception {
        withServer("<html>forbidden</html>", (context, tokens) -> {
            var refreshes = new AtomicInteger();
            Transportation transport = Wirespec.refreshingTransportation(context, c -> {
                refreshes.incrementAndGet();
                return fresh(c);
            });

            var e = failure(transport);

            assertEquals(403, e.status());
            assertEquals("<html>forbidden</html>", e.body());
            assertEquals(0, refreshes.get());
        });
    }

    @Test
    public void concurrentCallsRefreshOnce() throws Exception {
        withServer(AUTHENTICATION_ERROR, (context, tokens) -> {
            var refreshes = new AtomicInteger();
            Transportation transport = Wirespec.refreshingTransportation(context, c -> {
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

    @Test
    public void anExpiredContextIsRefreshedBeforeTheFirstRequestAndTheCallbackFiresOnce() throws Exception {
        withServer(AUTHENTICATION_ERROR, Instant.now().minusSeconds(1), (context, tokens) -> {
            var refreshes = new AtomicInteger();
            var changes = Collections.synchronizedList(new java.util.ArrayList<String>());
            Transportation transport = Wirespec.refreshingTransportation(context, c -> {
                refreshes.incrementAndGet();
                return fresh(c);
            }, c -> changes.add(c.sessionToken()));

            assertEquals(200, transport.transport(REQUEST).join().statusCode());

            assertEquals(1, refreshes.get());
            assertEquals(List.of("stale"), tokens);
            assertEquals(List.of("stale"), changes);
        });
    }

    @Test
    public void aContextThatIsNotExpiredIsNotRefreshed() throws Exception {
        withServer(AUTHENTICATION_ERROR, (context, tokens) -> {
            var refreshes = new AtomicInteger();
            REVIVED.set(true);
            Transportation transport = Wirespec.refreshingTransportation(context, c -> {
                refreshes.incrementAndGet();
                return c;
            }, c -> refreshes.incrementAndGet());

            assertEquals(200, transport.transport(REQUEST).join().statusCode());

            assertEquals(0, refreshes.get());
            assertEquals(List.of("stale"), tokens);
        });
    }

    @Test
    public void a403RefreshCallsTheCallbackOnceWithTheNewContext() throws Exception {
        withServer(AUTHENTICATION_ERROR, (context, tokens) -> {
            var changes = Collections.synchronizedList(new java.util.ArrayList<String>());
            Transportation transport = Wirespec.refreshingTransportation(context, TransportationRefreshTest::fresh, c -> changes.add(c.sessionToken()));

            assertEquals(200, transport.transport(REQUEST).join().statusCode());

            assertEquals(List.of("stale"), changes);
        });
    }

    @Test
    public void concurrentCallsOnAnExpiredContextRefreshOnceWhenBunqKeepsTheSessionToken() throws Exception {
        withServer(AUTHENTICATION_ERROR, Instant.now().minusSeconds(1), (context, tokens) -> {
            var refreshes = new AtomicInteger();
            var changes = new AtomicInteger();
            Transportation transport = Wirespec.refreshingTransportation(context, c -> {
                try {
                    Thread.sleep(200);
                } catch (InterruptedException e) {
                    throw new IllegalStateException(e);
                }
                refreshes.incrementAndGet();
                return fresh(c);
            }, c -> changes.incrementAndGet());

            // the refresh runs on the calling thread, so the calls are made from separate threads
            var pool = java.util.concurrent.Executors.newFixedThreadPool(3);
            try {
                var calls = java.util.stream.IntStream.range(0, 3)
                        .mapToObj(i -> CompletableFuture.supplyAsync(() -> transport.transport(REQUEST).join().statusCode(), pool))
                        .toList();
                for (var call : calls) {
                    assertEquals(200, call.join());
                }
            } finally {
                pool.shutdown();
            }

            assertEquals(1, refreshes.get());
            assertEquals(1, changes.get());
        });
    }

    @Test
    public void aFailedRefreshBeforeSendingIsNotRepeatedAfterThe403() throws Exception {
        withServer(AUTHENTICATION_ERROR, Instant.now().minusSeconds(1), (context, tokens) -> {
            var refreshes = new AtomicInteger();
            Transportation transport = Wirespec.refreshingTransportation(context, c -> {
                refreshes.incrementAndGet();
                throw new IllegalStateException("429");
            });

            assertEquals(403, failure(transport).status());
            assertEquals(1, refreshes.get());
        });
    }

    @Test
    public void anExceptionFromTheCallbackBeforeSendingFailsTheFuture() throws Exception {
        withServer(AUTHENTICATION_ERROR, Instant.now().minusSeconds(1), (context, tokens) -> {
            Transportation transport = Wirespec.refreshingTransportation(context, TransportationRefreshTest::fresh, c -> {
                throw new IllegalStateException("callback");
            });

            var future = transport.transport(REQUEST);

            assertEquals("callback", assertThrows(CompletionException.class, future::join).getCause().getMessage());
        });
    }

    @Test
    public void aContextExpiringIn10SecondsIsRefreshed() throws Exception {
        withServer(AUTHENTICATION_ERROR, Instant.now().plusSeconds(10), (context, tokens) -> {
            var refreshes = new AtomicInteger();
            Transportation transport = Wirespec.refreshingTransportation(context, c -> {
                refreshes.incrementAndGet();
                return fresh(c);
            });

            assertEquals(200, transport.transport(REQUEST).join().statusCode());
            assertEquals(1, refreshes.get());
            assertEquals(List.of("stale"), tokens); // refreshed before sending: no rejected request first
        });
    }
}
