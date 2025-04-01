package community.flock.bunq.java.example;

import community.flock.bunq.java.BunqModelCopied;
import community.flock.bunq.java.BunqResponseRaw;
import community.flock.bunq.java.Context;
import community.flock.wirespec.java.Wirespec;
import community.flock.wirespec.java.Wirespec.Method;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpUriRequest;
import org.apache.http.client.methods.RequestBuilder;
import org.apache.http.entity.ByteArrayEntity;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

import static community.flock.bunq.java.BunqHeader.bunqHeaders;
import static community.flock.bunq.java.BunqHeader.mergeMaps;


public class WirespecRawRequestHandler {
    private static final Set<String> HEADERS_HANDLED_BY_HTTP_CLIENT = Set.of(
            "Cache-Control",
            "User-Agent",
            "X-Bunq-Language",
            "X-Bunq-Region",
            "X-Bunq-Client-Request-Id",
            "X-Bunq-Geolocation",
            "X-Bunq-Client-Authentication"
    );

    private final String baseUrl;
    private final HttpClient client;

    public WirespecRawRequestHandler(String baseUrl, HttpClient client) {
        this.baseUrl = baseUrl;
        this.client = client;
    }

    public Wirespec.RawResponse handle(Context context, Wirespec.RawRequest rawRequest, String wrapper) throws IOException {
        HttpUriRequest httpUriRequest = createHttpRequest(rawRequest, context);
        HttpResponse response = client.execute(httpUriRequest);
        return createBunqResponseRaw(response, wrapper);
    }

    private HttpUriRequest createHttpRequest(Wirespec.RawRequest rawRequest, Context context) {
        var path = String.join("/", rawRequest.path());
        var queryParams = rawRequest.queries().entrySet().stream()
                .map(entry -> entry.getKey() + "=" + String.join(",", entry.getValue()))
                .collect(Collectors.joining("&"));


        var url = baseUrl + "/" + path + (!queryParams.isEmpty() ? "?" + queryParams : "");

        RequestBuilder requestBuilder = switch (rawRequest.method()) {
            case "GET" -> RequestBuilder.get(url);
            case "PUT" -> RequestBuilder.put(url);
            case "POST" -> RequestBuilder.post(url);
            case "DELETE" -> RequestBuilder.delete(url);
            case "OPTIONS" -> RequestBuilder.options(url);
            case "HEAD" -> RequestBuilder.head(url);
            case "PATCH" -> RequestBuilder.patch(url);
            case "TRACE" -> RequestBuilder.trace(url);
            default -> throw new IllegalStateException("Unexpected value: " + rawRequest.method());
        };
        var body = rawRequest.body().getBytes(StandardCharsets.UTF_8);
        if (body.length > 0 ) {
            requestBuilder.setEntity(new ByteArrayEntity(body));
        }


        var specificRequestHeaders = rawRequest.headers().entrySet().stream()
                .filter(entry -> !HEADERS_HANDLED_BY_HTTP_CLIENT.contains(entry.getKey()))
                .collect(Collectors.toMap(Map.Entry::getKey, entry -> String.join(",", entry.getValue())));

        mergeMaps(specificRequestHeaders, bunqHeaders(wirespecMethod(rawRequest),rawRequest.body(), context))
                .forEach(requestBuilder::addHeader);

        return requestBuilder
                .build();
    }

    private Method wirespecMethod(Wirespec.RawRequest rawRequest) {
        return switch (rawRequest.method()) {
            case "GET" -> Method.GET;
            case "PUT" -> Method.PUT;
            case "POST" -> Method.POST;
            case "DELETE" -> Method.DELETE;
            case "OPTIONS" -> Method.OPTIONS;
            case "HEAD" -> Method.HEAD;
            case "PATCH" -> Method.PATCH;
            case "TRACE" -> Method.TRACE;
            default -> throw new IllegalStateException("Unexpected value: " + rawRequest.method());
        };
    }

    private Wirespec.RawResponse createBunqResponseRaw(HttpResponse response, String wrapper)
            throws IOException {
        int responseCode = response.getStatusLine().getStatusCode();
        byte[] responseBodyBytes = response.getEntity() != null ? response.getEntity().getContent().readAllBytes() : new byte[0];


        //TODO: do validate?
//        assertResponseSuccess(responseCode, responseBodyBytes, getResponseId(response));
//        validateResponseSignature(responseCode, responseBodyBytes, response);

        BunqResponseRaw bunqResponseRaw = new BunqResponseRaw(responseBodyBytes,
                Arrays.stream(response.getAllHeaders()).toList().stream()
                        .collect(Collectors.toMap(
                                        NameValuePair::getName,
                                        NameValuePair::getValue
                                )
                        )
        );

        String rawBody;
        if (wrapper == null) {
            rawBody = BunqModelCopied.fromJsonToRawResponse(bunqResponseRaw);
        } else {
            rawBody = BunqModelCopied.fromJsonToRawResponse(bunqResponseRaw, wrapper);

        }
        return new Wirespec.RawResponse(
                responseCode,
                bunqResponseRaw.getHeaders().entrySet().stream()
                        .collect(Collectors.toMap(Map.Entry::getKey, entry -> List.of(entry.getValue()))),
                rawBody
        );
    }

}
