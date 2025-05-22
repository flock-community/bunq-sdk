package com.bunq.sdk;

import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.fasterxml.jackson.datatype.jdk8.Jdk8Module;
import com.fasterxml.jackson.module.kotlin.KotlinModule;
import community.flock.wirespec.integration.jackson.java.WirespecModuleJava;
import community.flock.wirespec.java.serde.DefaultParamSerialization;

import java.io.IOException;
import java.lang.reflect.Method;
import java.lang.reflect.ParameterizedType;
import java.lang.reflect.Type;
import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.CompletableFuture;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.StreamSupport;

public class Wirespec {
    public static final String baseUrl = "https://public-api.sandbox.bunq.com/v1/";

    public static final ObjectMapper objectMapper;

    static {
        objectMapper = new ObjectMapper()
                .configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false)
                .registerModule(new KotlinModule.Builder().build())
                .registerModule(new WirespecModuleJava())
                .registerModule(new Jdk8Module());
    }

    public static final community.flock.wirespec.Wirespec.Serialization<String> serialization = new BunqSerialization();

    public static CompletableFuture<community.flock.wirespec.Wirespec.RawResponse> send(Signing signing, community.flock.wirespec.Wirespec.RawRequest req) {
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
                .thenApply(response -> new community.flock.wirespec.Wirespec.RawResponse(
                        response.statusCode(),
                        response.headers().map(),
                        response.body()
                ));
    }

    private static class BunqSerialization implements community.flock.wirespec.Wirespec.Serialization<String>, DefaultParamSerialization {
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

    public static <Req extends community.flock.wirespec.Wirespec.Request<?>, Res extends community.flock.wirespec.Wirespec.Response<?>> Function<Req,CompletableFuture<Res>> handler(
            Signing signing, Context context) {
        return (request -> {
            try {
                // Get the declaring class of the request
                Class<?> declaringClass = request.getClass().getDeclaringClass();

                // Find the Handler class
                Class<?> handlerClass = Arrays.stream(declaringClass.getDeclaredClasses())
                        .filter(clazz -> clazz.getSimpleName().equals("Handler"))
                        .findFirst()
                        .orElseThrow(() -> new RuntimeException("Handler not found"));

                // Find the Handlers class
                Class<?> handlersClass = Arrays.stream(handlerClass.getDeclaredClasses())
                        .filter(clazz -> clazz.getSimpleName().equals("Handlers"))
                        .findFirst()
                        .orElseThrow(() -> new RuntimeException("Handler not found"));

                //create instance of handlers class
                Object handlersInstance = handlersClass.getDeclaredConstructor().newInstance();

                // Get the client method from the Handler class
                // From the Handlers interface, there is a class Handlers, inside a getClient Method
                Method clientMethod = Arrays.stream(handlersClass.getDeclaredMethods())
                        .filter(method -> method.getName().equals("getClient"))
                        .findFirst()
                        .orElseThrow(() -> new RuntimeException("client method not found"));

                // Invoke the client method to get the client instance
                Object client = clientMethod.invoke(handlersInstance, serialization);

                // Get the to method from the client
                Method toMethod = client.getClass().getMethod("to", community.flock.wirespec.Wirespec.Request.class);
                toMethod.setAccessible(true);

                // Invoke the to method to get the raw request
                community.flock.wirespec.Wirespec.RawRequest rawRequest = (community.flock.wirespec.Wirespec.RawRequest) toMethod.invoke(client, request);

                // Add the authentication header
                Map<String, List<String>> headers = new HashMap<>(rawRequest.headers());
                headers.put("X-Bunq-Client-Authentication", java.util.List.of(context.getSessionToken()));

                // Create a new raw request with the updated headers
                community.flock.wirespec.Wirespec.RawRequest reqToken = new community.flock.wirespec.Wirespec.RawRequest(
                        rawRequest.method(),
                        rawRequest.path(),
                        rawRequest.queries(),
                        headers,
                        rawRequest.body()
                );

                // Send the request
                return send(signing, reqToken).thenApply(raw -> {
                            try {
                                // Get the from method from the client
                                Method fromMethod = client.getClass().getMethod("from", community.flock.wirespec.Wirespec.RawResponse.class);
                                fromMethod.setAccessible(true);
                                // Invoke the from method to get the response
                                return (Res) fromMethod.invoke(client, raw);
                            } catch (Exception e) {
                                throw new RuntimeException("Failed to handle request", e);
                            }
                        }
                );

            } catch (Exception e) {
                throw new RuntimeException("Failed to handle request", e);
            }
        });
    }
}
