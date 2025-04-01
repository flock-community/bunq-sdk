package org.example;

import com.bunq.sdk.http.BunqResponse;
import community.flock.bunq.java.BunqHeader;
import community.flock.bunq.java.BunqResponseRaw;
import community.flock.bunq.java.example.GsonBunqSerializer;
import community.flock.wirespec.generated.java.CREATE_RequestInquiry_for_User_MonetaryAccount400ResponseBody;
import community.flock.wirespec.generated.java.CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint;
import community.flock.wirespec.generated.java.ErrorArray;
import community.flock.wirespec.generated.java.MonetaryAccountBankRead;
import community.flock.wirespec.generated.java.READ_MonetaryAccountBank_for_User400ResponseBody;
import community.flock.wirespec.generated.java.READ_MonetaryAccountBank_for_UserEndpoint;
import community.flock.wirespec.generated.java.RequestInquiryCreate;
import community.flock.wirespec.java.Wirespec;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.nio.charset.StandardCharsets;
import java.security.KeyPair;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.CompletableFuture;
import java.util.stream.Collectors;

import static com.bunq.sdk.context.BunqContext.getApiContext;
import static java.util.Optional.empty;
import static community.flock.bunq.java.SecurityUtils.generateSignature;

public class MonetaryAccountClientV3 implements READ_MonetaryAccountBank_for_UserEndpoint.Handler, CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Handler {
    private static final Logger logger = LoggerFactory.getLogger(MonetaryAccountClientV3.class);
    private static final Set<String> HEADERS_HANDLED_BY_HTTP_CLIENT = Set.of(
            "Cache-Control",
            "User-Agent",
            "X-Bunq-Language",
            "X-Bunq-Region",
            "X-Bunq-Client-Request-Id",
            "X-Bunq-Geolocation",
            "X-Bunq-Client-Authentication"
    );
    private final GsonBunqSerializer serialization = new GsonBunqSerializer();

    private String sessionToken;
    private KeyPair keyPair;

    @Override
    public CompletableFuture<READ_MonetaryAccountBank_for_UserEndpoint.Response<?>> rEAD_MonetaryAccountBank_for_User(READ_MonetaryAccountBank_for_UserEndpoint.Request request) {
        if (sessionToken == null || keyPair == null) {
            throw new IllegalStateException("SessionToken and KeyPair must be set before calling this method.");
        }

        int accountId = Math.toIntExact(request.getPath().itemId());

        Wirespec.RawRequest rawRequest = READ_MonetaryAccountBank_for_UserEndpoint.Handler.toRequest(serialization, request);

        ForkedApiClient apiClient = new ForkedApiClient(getApiContext());
        var path = String.join("/", rawRequest.path());
        var params = rawRequest.queries().entrySet().stream().collect(Collectors.toMap(
                Map.Entry::getKey,
                entry -> String.join(",", entry.getValue())));
        var specificRequestHeaders = rawRequest.headers().entrySet().stream()
                .filter(it -> !HEADERS_HANDLED_BY_HTTP_CLIENT.contains(it.getKey()))
                .collect(Collectors.toMap(
                        Map.Entry::getKey,
                        entry -> String.join(",", entry.getValue())));
        Map<String, String> allHeaders = mergeMaps(specificRequestHeaders, bunqHeaders(request.getMethod(), rawRequest.body(), keyPair, sessionToken));

        return CompletableFuture.supplyAsync(() -> {
                    BunqResponseRaw responseRaw = apiClient.get(path, params, allHeaders);
                    BunqResponse<MonetaryAccountBankRead> monetaryAccountBank = BunqModell.fromJson(MonetaryAccountBankRead.class, responseRaw, "MonetaryAccountBank");
                    return monetaryAccountBank.getValue();
                })
                .<READ_MonetaryAccountBank_for_UserEndpoint.Response<?>>thenApply(it ->
                        new READ_MonetaryAccountBank_for_UserEndpoint.Response200(
                                empty(), // not-needed?
                                empty(), // not-needed?
                                empty(), // not-needed?
                                it)
                ).exceptionally(it -> {
                    logger.error("Something went wrong fetching MonetaryAccountBank with accountId {}", accountId, it);
                    return new READ_MonetaryAccountBank_for_UserEndpoint.Response400(
                            empty(), // not-needed?
                            empty(), // not-needed?
                            empty(), // not-needed?
                            to400Response(it));
                });
    }

    @Override
    public CompletableFuture<CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Response<?>> cREATE_RequestInquiry_for_User_MonetaryAccount(CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Request request) {
        {
            if (sessionToken == null || keyPair == null) {
                throw new IllegalStateException("SessionToken and KeyPair must be set before calling this method.");
            }

            Wirespec.RawRequest rawRequest = CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Handler.toRequest(serialization, request);

            ForkedApiClient apiClient = new ForkedApiClient(getApiContext());
            var path = String.join("/", rawRequest.path());
            var specificRequestHeaders = rawRequest.headers().entrySet().stream()
                    .filter(it -> !HEADERS_HANDLED_BY_HTTP_CLIENT.contains(it.getKey()))
                    .collect(Collectors.toMap(
                            Map.Entry::getKey,
                            entry -> String.join(",", entry.getValue())));
            Map<String, String> allHeaders = mergeMaps(specificRequestHeaders, bunqHeaders(request.getMethod(), rawRequest.body(), keyPair, sessionToken));

            var body = rawRequest.body().getBytes(StandardCharsets.UTF_8);
            return CompletableFuture.supplyAsync(() -> {
                        BunqResponseRaw responseRaw = apiClient.post(path, body, allHeaders);
                        BunqResponse<RequestInquiryCreate> monetaryAccountBank = BunqModell.fromJson(RequestInquiryCreate.class, responseRaw);
                        return monetaryAccountBank.getValue();
                    })
                    .<CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Response<?>>thenApply(it ->
                            new CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Response200(
                                    empty(), // not-needed?
                                    empty(), // not-needed?
                                    empty(), // not-needed?
                                    it)
                    ).exceptionally(it -> {
                        logger.error("Something went wrong creating money ", it);
                        return new CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Response400(
                                empty(), // not-needed?
                                empty(), // not-needed?
                                empty(), // not-needed?
                                to400ResponseX(it));
                    });
        }
    }

    private READ_MonetaryAccountBank_for_User400ResponseBody to400Response(Throwable it) {
        return new READ_MonetaryAccountBank_for_User400ResponseBody(
                Optional.of(
                        List.of(
                                new ErrorArray(
                                        Optional.of(it.getMessage()),
                                        Optional.empty()
                                )
                        )
                )
        );
    }
    private CREATE_RequestInquiry_for_User_MonetaryAccount400ResponseBody to400ResponseX(Throwable it) {
        return new CREATE_RequestInquiry_for_User_MonetaryAccount400ResponseBody(
                Optional.of(
                        List.of(
                                new ErrorArray(
                                        Optional.of(it.getMessage()),
                                        Optional.empty()
                                )
                        )
                )
        );
    }


    private Map<String, String> bunqHeaders(Wirespec.Method method, String body, KeyPair keyPair, String sessionToken) {
        return mergeMaps(defaultHeaders(), sessionHeaders(method, body, keyPair, sessionToken));
    }

    /**
     *
     */
    private Map<String, String> defaultHeaders() {
        HashMap<String, String> map = new HashMap<>();
        BunqHeader.CACHE_CONTROL.addTo(map, null);
        BunqHeader.USER_AGENT.addTo(map, null);
        BunqHeader.LANGUAGE.addTo(map, null);
        BunqHeader.REGION.addTo(map, null);
        BunqHeader.CLIENT_REQUEST_ID.addTo(map, UUID.randomUUID().toString());
        BunqHeader.GEOLOCATION.addTo(map, null);
        return map;
    }

    /**
     *
     */
    private Map<String, String> sessionHeaders(Wirespec.Method method, String body, KeyPair keyPair, String sessionToken) {

        if (sessionToken != null) {
            var map = new HashMap<String, String>();
            BunqHeader.CLIENT_AUTHENTICATION.addTo(map, sessionToken);
            BunqHeader.CLIENT_SIGNATURE.addTo(map, generateSignature(method, body, keyPair));
            return map;
        }
        return new HashMap<>();
    }


    public void setSessionToken(String sessionToken) {
        this.sessionToken = sessionToken;
    }

    public void setKeyPair(KeyPair keyPair) {
        this.keyPair = keyPair;
    }

    /**
     * Combines two maps into a new map. If there are duplicate keys, values from the second map will override the first.
     */
    private static Map<String, String> mergeMaps(Map<String, String> map1, Map<String, String> map2) {
        return new HashMap<>() {{
            putAll(map1);
            putAll(map2);
        }};
    }
}
