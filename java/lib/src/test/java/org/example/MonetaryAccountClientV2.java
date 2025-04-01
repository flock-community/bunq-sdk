package org.example;

import com.bunq.sdk.http.ApiClient;
import com.bunq.sdk.http.BunqResponse;
import com.bunq.sdk.http.BunqResponseRaw;
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
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.concurrent.CompletableFuture;
import java.util.stream.Collectors;

import static com.bunq.sdk.context.BunqContext.getApiContext;
import static java.util.Optional.empty;

public class MonetaryAccountClientV2 implements READ_MonetaryAccountBank_for_UserEndpoint.Handler, CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Handler {
    private static final Logger logger = LoggerFactory.getLogger(MonetaryAccountClientV2.class);
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

    @Override
    public CompletableFuture<READ_MonetaryAccountBank_for_UserEndpoint.Response<?>> rEAD_MonetaryAccountBank_for_User(READ_MonetaryAccountBank_for_UserEndpoint.Request request) {
        Wirespec.RawRequest rawRequest = READ_MonetaryAccountBank_for_UserEndpoint.Handler.toRequest(serialization, request);

        ApiClient apiClient = new ApiClient(getApiContext());
        var headers = rawRequest.headers().entrySet().stream()
                .filter(it -> !HEADERS_HANDLED_BY_HTTP_CLIENT.contains(it.getKey()))
                .collect(Collectors.toMap(
                        Map.Entry::getKey,
                        entry -> String.join(",", entry.getValue())));
        var params = rawRequest.queries().entrySet().stream().collect(Collectors.toMap(
                Map.Entry::getKey,
                entry -> String.join(",", entry.getValue())));

        return CompletableFuture.supplyAsync(() -> {
                    BunqResponseRaw responseRaw = apiClient.get(String.join("/", rawRequest.path()), params, headers);
                    BunqResponse<MonetaryAccountBankRead> monetaryAccountBank = BunqModell.fromJson(MonetaryAccountBankRead.class, new community.flock.bunq.java.BunqResponseRaw(responseRaw.getBodyBytes(), responseRaw.getHeaders()), "MonetaryAccountBank");
                    return monetaryAccountBank.getValue();
                })
                .<READ_MonetaryAccountBank_for_UserEndpoint.Response<?>>thenApply(it ->
                        new READ_MonetaryAccountBank_for_UserEndpoint.Response200(
                                empty(), // not-needed?
                                empty(), // not-needed?
                                empty(), // not-needed?
                                it)
                ).exceptionally(it -> {
                    logger.error("Something went wrong fetching MonetaryAccountBank for userId {}", request.getPath().userID(), it);
                    return new READ_MonetaryAccountBank_for_UserEndpoint.Response400(
                            empty(), // not-needed?
                            empty(), // not-needed?
                            empty(), // not-needed?
                            to400Response(it));
                });
    }

    @Override
    public CompletableFuture<CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Response<?>> cREATE_RequestInquiry_for_User_MonetaryAccount(CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Request request) {
        Wirespec.RawRequest rawRequest = CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Handler.toRequest(serialization, request);

        ApiClient apiClient = new ApiClient(getApiContext());
        var headers = rawRequest.headers().entrySet().stream()
                .filter(it -> !HEADERS_HANDLED_BY_HTTP_CLIENT.contains(it.getKey()))
                .collect(Collectors.toMap(
                        Map.Entry::getKey,
                        entry -> String.join(",", entry.getValue())));

        byte[] body = rawRequest.body().getBytes(StandardCharsets.UTF_8);

        return CompletableFuture.supplyAsync(() -> {
                    BunqResponseRaw responseRaw = apiClient.post(String.join("/", rawRequest.path()), body, headers);
                    BunqResponse<RequestInquiryCreate> requestInquiryBunqResponse = BunqModell
                            .fromJson(RequestInquiryCreate.class, new community.flock.bunq.java.BunqResponseRaw(responseRaw.getBodyBytes(), responseRaw.getHeaders()));
                    return requestInquiryBunqResponse.getValue();
                })
                .<CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Response<?>>thenApply(it ->
                        new CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Response200(
                                empty(), // not-needed?
                                empty(), // not-needed?
                                empty(), // not-needed?
                                it)
                ).exceptionally(it -> {
                    logger.error("Something went wrong fetching MonetaryAccountBank for userId {}", request.getPath().userID(), it);
                    return new CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Response400(
                            empty(), // not-needed?
                            empty(), // not-needed?
                            empty(), // not-needed?
                            to400ResponseX(it));
                });
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
}
