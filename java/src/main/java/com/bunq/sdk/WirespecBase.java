package com.bunq.sdk;

import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.fasterxml.jackson.datatype.jdk8.Jdk8Module;
import com.fasterxml.jackson.module.kotlin.KotlinModule;
import community.flock.wirespec.integration.jackson.java.WirespecModuleJava;
import community.flock.wirespec.java.Wirespec;
import community.flock.wirespec.java.serde.DefaultParamSerialization;

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
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.stream.Collectors;
import java.util.stream.StreamSupport;

public class WirespecBase {
    public static final String baseUrl = "https://public-api.sandbox.bunq.com/v1/";

    public static final ObjectMapper objectMapper;

    static {
        objectMapper = new ObjectMapper()
                .configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false)
                .registerModule(new KotlinModule.Builder().build())
                .registerModule(new WirespecModuleJava())
                .registerModule(new Jdk8Module());
    }

    public static final Wirespec.Serialization<String> serialization = new BunqSerialization();

    public static CompletableFuture<Wirespec.RawResponse> send(Signing signing, Wirespec.RawRequest req) {
        HttpClient client = HttpClient.newBuilder().build();

        // Build the URI
        String pathString = String.join("/", req.path());
        URI baseUri = URI.create(baseUrl + pathString);
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
        if (req.body() != null) {
            headersList.add("X-Bunq-Client-Signature");
            headersList.add(signing.signData(req.body()));
            headers = headersList.toArray(new String[0]);
        } else {
            headers = headersList.toArray(new String[0]);
        }

        // Build the request
        HttpRequest.Builder requestBuilder = HttpRequest.newBuilder()
                .uri(uri)
                .method(
                        req.method().toUpperCase(),
                        req.body() != null
                                ? HttpRequest.BodyPublishers.ofString(req.body())
                                : HttpRequest.BodyPublishers.noBody()
                )
                .headers(headers);

        return client.sendAsync(requestBuilder.build(), HttpResponse.BodyHandlers.ofString())
                .thenApply(response -> new Wirespec.RawResponse(
                        response.statusCode(),
                        response.headers().map(),
                        response.body()
                ));
    }

    private static class BunqSerialization implements Wirespec.Serialization<String>, DefaultParamSerialization {
        @Override
        public <T> String serialize(T t, Type type) {
            if (t == null) {
                return null;
            }
            try {

                return objectMapper.writeValueAsString(t);
            } catch (Exception e) {
                throw new RuntimeException("Failed to serialize object", e);
            }
        }

        @Override
        public <T> List<String> serializeParam(T value, Type type) {
            return DefaultParamSerialization.super.serializeParam(value, type);
        }

        @Override
        public <T> T deserialize(String raw, Type type) {
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

            ObjectNode json = null;
            // Reduce the ObjectNodes to a single ObjectNode
            for (ObjectNode node : objectNodes) {
                if (json == null) {
                    json = node;
                } else {
                    json.setAll(node);
                }
            }
            return json;
        }

    }
}
