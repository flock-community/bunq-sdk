package com.bunq.sdk;

import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.fasterxml.jackson.datatype.jdk8.Jdk8Module;
import com.fasterxml.jackson.module.kotlin.KotlinModule;
import community.flock.wirespec.integration.jackson.v2.java.WirespecModuleJava;
import community.flock.wirespec.java.Wirespec.RawRequest;
import community.flock.wirespec.java.Wirespec.RawResponse;
import community.flock.wirespec.java.Wirespec.Serialization;
import community.flock.wirespec.java.Wirespec.Transportation;
import com.bunq.sdk.generated.Client;
import community.flock.wirespec.java.serde.DefaultParamSerialization;
import community.flock.wirespec.java.serde.DefaultPathSerialization;

import java.io.IOException;
import java.lang.reflect.ParameterizedType;
import java.lang.reflect.Type;
import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.atomic.AtomicReference;
import java.util.concurrent.locks.ReentrantLock;
import java.util.function.UnaryOperator;
import java.util.stream.Collectors;
import java.util.stream.StreamSupport;

public class Wirespec {
        public static final ObjectMapper objectMapper;

    static {
        objectMapper = new ObjectMapper()
                .configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false)
                .registerModule(new KotlinModule.Builder().build())
                .registerModule(new WirespecModuleJava())
                .registerModule(new Jdk8Module());
    }

    public static final Serialization serialization = new BunqSerialization();

    private static final HttpClient client = HttpClient.newBuilder().build();

    public static CompletableFuture<RawResponse> send(Config config, RawRequest req) {
        // Build the URI
        String pathString = String.join("/", req.path());
        URI baseUri = URI.create(config.bunqServer().baseUrl() + pathString);
        URI uri;

        if (!req.queries().isEmpty()) {
            String queryString = req.queries().entrySet().stream()
                    .flatMap(entry -> entry.getValue().stream()
                            .map(v -> entry.getKey() + "=" + URLEncoder.encode(v, StandardCharsets.UTF_8)))
                    .collect(Collectors.joining("&"));
            uri = URI.create(baseUri + "?" + queryString);
        } else {
            uri = baseUri;
        }

        // Process headers
        List<String> headersList = new ArrayList<>();
        headersList.add("User-Agent");
        headersList.add(config.userAgent() != null && !config.userAgent().isBlank() ? config.userAgent() : config.serviceName());
        req.headers().forEach((key, values) -> {
            values.stream()
                    .filter(value -> !value.isBlank())
                    .forEach(value -> {
                        headersList.add(key);
                        headersList.add(value);
                    });
        });

        // Sign request if body is present
        String[] headers;
        if (req.body().isPresent()) {
            headersList.add("X-Bunq-Client-Signature");
            headersList.add(Signing.signData(config, new String(req.body().get(), StandardCharsets.UTF_8)));
            headers = headersList.toArray(new String[0]);
        } else {
            headers = headersList.toArray(new String[0]);
        }

        // Build the request
        HttpRequest.Builder requestBuilder = HttpRequest.newBuilder()
                .uri(uri)
                .method(
                        req.method().toUpperCase(),
                        req.body().isPresent()
                                ? HttpRequest.BodyPublishers.ofByteArray(req.body().get())
                                : HttpRequest.BodyPublishers.noBody()
                )
                .headers(headers);

        return client.sendAsync(requestBuilder.build(), HttpResponse.BodyHandlers.ofByteArray())
                .thenApply(response -> new RawResponse(
                        response.statusCode(),
                        response.headers().map(),
                        Optional.ofNullable(response.body())
                ));
    }

    private static class BunqSerialization implements Serialization, DefaultParamSerialization, DefaultPathSerialization {
        @Override
        public <T> byte[] serializeBody(T t, Type type) {
            if (t == null) {
                return null;
            }
            try {
                return objectMapper.writeValueAsBytes(t);
            } catch (Exception e) {
                throw new RuntimeException("Failed to serialize object", e);
            }
        }

        @Override
        public <T> List<String> serializeParam(T value, Type type) {
            return DefaultParamSerialization.super.serializeParam(value, type);
        }

        @Override
        public <T> T deserializeBody(byte[] raw, Type type) {
            try {
                var tree = objectMapper.readTree(raw);
                var response = tree.get("Response");
                Object json = aggregateJsonNodes(type, response);
                return objectMapper.convertValue(json, objectMapper.constructType(type));
            } catch (IOException e) {
                throw new RuntimeException("Failed to deserialize JSON", e);
            }
        }

        private static Object aggregateJsonNodes(Type type, JsonNode response) {
            // Convert the response to an iterable and filter for ObjectNode instances
            Iterable<ObjectNode> objectNodes = () -> StreamSupport.stream(response.spliterator(), false)
                    .filter(node -> node instanceof ObjectNode)
                    .map(node -> (ObjectNode) node)
                    .iterator();

            if (type instanceof ParameterizedType parameterizedType && parameterizedType.getRawType() == List.class) {
                ArrayNode json = objectMapper.createArrayNode();
                // Reduce the ObjectNodes to a single ObjectNode
                for (ObjectNode node : objectNodes) {
                    node.fieldNames().forEachRemaining(fieldName -> {
                        json.add(node.get(fieldName));
                    });
                }
                return json;
            }

            ObjectNode json = objectMapper.createObjectNode();
            // Reduce the ObjectNodes to a single ObjectNode; an empty response yields an empty object
            for (ObjectNode node : objectNodes) {
                json.setAll(node);
            }
            return json;
        }

    }

    public static Client bunqClient(Context context) {
        return new Client(serialization, transportation(context));
    }

    /**
     * Sends requests with the context's authentication headers.
     * bunq answers a dead session with 403 "Insufficient authentication."; the session is then refreshed once
     * and the request is retried with the new session token. Any other 403 is returned as is, as is the original
     * response when the refresh itself fails. The refreshed context is kept inside this transportation.
     */
    public static Transportation transportation(Context context) {
        return transportation(context, Context::refreshSession);
    }

    static Transportation transportation(Context context, UnaryOperator<Context> refresh) {
        var current = new AtomicReference<>(context);
        var lock = new ReentrantLock();

        return request -> {
            Context used = current.get();
            return sendWith(used, request).thenCompose(response -> {
                if (!isSessionRejected(response)) {
                    return CompletableFuture.completedFuture(response);
                }
                Context refreshed;
                lock.lock();
                try {
                    // another request may have refreshed the session while this one waited
                    if (!current.get().sessionToken().equals(used.sessionToken())) {
                        refreshed = current.get();
                    } else {
                        refreshed = refresh.apply(used);
                        current.set(refreshed);
                    }
                } catch (RuntimeException e) {
                    logger.log(System.Logger.Level.WARNING, "bunq session refresh failed: " + e.getMessage());
                    return CompletableFuture.completedFuture(response);
                } finally {
                    lock.unlock();
                }
                return sendWith(refreshed, request);
            });
        };
    }

    private static final System.Logger logger = System.getLogger(Wirespec.class.getName());

    private static CompletableFuture<RawResponse> sendWith(Context context, RawRequest request) {
        Map<String, List<String>> headers = new HashMap<>(request.headers());
        headers.putAll(toHeaders(context));
        return send(context.config(), new RawRequest(request.method(), request.path(), request.queries(), headers, request.body()));
    }

    static Map<String, List<String>> toHeaders(Context context) {
        Map<String, List<String>> headers = new HashMap<>();
        headers.put("X-Bunq-Client-Authentication", List.of(context.sessionToken()));
        var config = context.config();
        putIfPresent(headers, "Cache-Control", config.cacheControl());
        putIfPresent(headers, "X-Bunq-Language", config.language());
        putIfPresent(headers, "X-Bunq-Region", config.region());
        putIfPresent(headers, "X-Bunq-Client-Request-Id", config.clientRequestId());
        putIfPresent(headers, "X-Bunq-GeoLocation", config.geolocation());
        return headers;
    }

    private static void putIfPresent(Map<String, List<String>> headers, String name, String value) {
        if (value != null) {
            headers.put(name, List.of(value));
        }
    }

    private static boolean isSessionRejected(RawResponse response) {
        if (response.statusCode() != 403 || response.body().isEmpty()) {
            return false;
        }
        try {
            for (JsonNode error : objectMapper.readTree(response.body().get()).get("Error")) {
                if ("Insufficient authentication.".equals(error.path("error_description").asText(null))) {
                    return true;
                }
            }
        } catch (IOException | RuntimeException e) {
            return false;
        }
        return false;
    }
}
