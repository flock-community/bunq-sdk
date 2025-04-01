package org.example;

import com.bunq.sdk.context.ApiContext;
import com.bunq.sdk.context.ApiEnvironmentType;
import com.bunq.sdk.context.BunqContext;
import com.bunq.sdk.context.InstallationContext;
import com.bunq.sdk.exception.ApiException;
import com.bunq.sdk.exception.ExceptionFactory;
import com.bunq.sdk.exception.UncaughtExceptionError;
import com.bunq.sdk.http.BunqHeader;
import com.bunq.sdk.http.BunqRequestBuilder;
import com.bunq.sdk.http.BunqResponseRaw;
import com.bunq.sdk.http.Pagination;
import com.bunq.sdk.json.BunqGsonBuilder;
import com.bunq.sdk.model.generated.endpoint.MonetaryAccountBank;
import com.bunq.sdk.security.SecurityUtils;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonSyntaxException;
import community.flock.bunq.java.Context;
import community.flock.bunq.java.example.MonetaryAccountClientV4;
import community.flock.bunq.java.example.WirespecRawRequestHandler;
import community.flock.wirespec.generated.java.Amount;
import community.flock.wirespec.generated.java.CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint;
import community.flock.wirespec.generated.java.MonetaryAccountBankRead;
import community.flock.wirespec.generated.java.Pointer;
import community.flock.wirespec.generated.java.READ_MonetaryAccountBank_for_User400ResponseBody;
import community.flock.wirespec.generated.java.READ_MonetaryAccountBank_for_UserEndpoint;
import community.flock.wirespec.generated.java.RequestInquiry;
import community.flock.wirespec.generated.java.RequestInquiryCreate;
import flock.community.bunq_sdk.java.BunqRepository;
import okhttp3.HttpUrl;
import okhttp3.Request;
import okhttp3.Response;
import org.apache.http.impl.client.HttpClients;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.SortedMap;
import java.util.TreeMap;
import java.util.UUID;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;
import java.util.regex.Pattern;

import static com.bunq.sdk.context.BunqContext.getApiContext;
import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.fail;

public class BunqRepositoryTest {
    private static final Logger logger = LoggerFactory.getLogger(BunqRepositoryTest.class);
    /**
     * Borrowed from sdk
     */
    private static final String FIELD_ERROR = "Error";
    private static final String FIELD_ERROR_DESCRIPTION = "error_description";

    /**
     * end borrow from sdk
     */


    private final Gson gson = BunqGsonBuilder.buildDefault().create();

    private static ApiContext apiContext;
    private static READ_MonetaryAccountBank_for_UserEndpoint.Request wirespecGetRequest;
    private static CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Request wirespecPostRequest;

    @BeforeAll
    public static void setupBunqRepositoryAndClient() throws UnknownHostException {
        BunqRepository repository = new BunqRepository(
                ApiEnvironmentType.SANDBOX,
                "none",
                true
        );
        apiContext = getApiContext();

        int monetaryAccountBankId = getSandboxAccountId(); // not using any wirespec here.
        Integer userId = BunqContext.getUserContext().getUserId();

        wirespecGetRequest = new READ_MonetaryAccountBank_for_UserEndpoint.Request(
                userId.longValue(),
                (long) monetaryAccountBankId,
                Optional.empty(),       // <-- Cache-Control via intermediate
                "useragent",                        // <-- useragent via
                Optional.empty(),                   // <-- xbungLanguage
                Optional.empty(),                   // <-- xbungregion
                Optional.empty(),                   // <-- xbungclientrequestId
                Optional.empty(),                   // <-- xbunqGeoLocation
                "xbunqclientauthentication"         // <-- xbunqClientAuth
        );

        wirespecPostRequest = new CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Request(
                userId.longValue(),
                (long) monetaryAccountBankId,
                Optional.empty(),       // <-- Cache-Control via intermediate
                "useragent",                        // <-- useragent via
                Optional.empty(),                   // <-- xbungLanguage
                Optional.empty(),                   // <-- xbungregion
                Optional.empty(),                   // <-- xbungclientrequestId
                Optional.empty(),                   // <-- xbunqGeoLocation
                "xbunqclientauthentication",         // <-- xbunqClientAuth
                new RequestInquiry(
                        Optional.of(new Amount(Optional.of("13.37"), Optional.of("EUR"))),
                        Optional.of(new Pointer(
                                Optional.of("EMAIL"),
                                Optional.of("sugardaddy@bunq.com"),
                                Optional.empty(),
                                Optional.empty()

                        )),
                        Optional.of("Requesting some spending money."),
                        Optional.empty(),
                        Optional.empty(),
                        Optional.empty(),
                        Optional.empty(),
                        Optional.empty(),
                        Optional.empty(),
                        Optional.empty(),
                        Optional.empty(),
                        true,
                        Optional.empty(),
                        Optional.empty(),
                        Optional.empty(),
                        Optional.empty(),
                        Optional.empty(),
                        Optional.empty(),
                        Optional.empty(),
                        Optional.empty(),
                        Optional.empty(),
                        Optional.empty(),
                        Optional.empty(),
                        Optional.empty(),
                        Optional.empty(),
                        Optional.empty(),
                        Optional.empty(),
                        Optional.empty(),
                        Optional.empty(),
                        Optional.empty()
                )
        );

        logger.info("BunqRepositoryTest setupBunqRepositoryAndClient done");
        logger.info("===");
        logger.info("===");
    }

    @AfterEach
    void blub() {
        logger.info("===");
        logger.info("===");

    }

    @Test
    public void testGetMonetaryBankAccountThroughSDK() throws ExecutionException, InterruptedException, TimeoutException {
        CompletableFuture<READ_MonetaryAccountBank_for_UserEndpoint.Response<?>> responseCompletableFuture =
                new MonetaryAccountClientV1().rEAD_MonetaryAccountBank_for_User(wirespecGetRequest);

        // response mapping
        validateResponseGet(responseCompletableFuture);


        CompletableFuture<CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Response<?>> responseCompletableFuturePost =
                new MonetaryAccountClientV1().cREATE_RequestInquiry_for_User_MonetaryAccount(wirespecPostRequest);

        // response mapping
        validateResponsePost(responseCompletableFuturePost);


    }


    @Test
    void testSomeLevelOfIntermediateMapping() throws ExecutionException, InterruptedException, TimeoutException {
        CompletableFuture<READ_MonetaryAccountBank_for_UserEndpoint.Response<?>> responseCompletableFuture =
                new MonetaryAccountClientV2().rEAD_MonetaryAccountBank_for_User(wirespecGetRequest);


        // response mapping
        validateResponseGet(responseCompletableFuture);

        CompletableFuture<CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Response<?>> responseCompletableFuturePost =
                new MonetaryAccountClientV2().cREATE_RequestInquiry_for_User_MonetaryAccount(wirespecPostRequest);

        // response mapping
        validateResponsePost(responseCompletableFuturePost);

    }

    @Test
    void testSomeLevelOfIntermediateMapping2() throws ExecutionException, InterruptedException, TimeoutException {
        var clientV3 = new MonetaryAccountClientV3();
        clientV3.setKeyPair(apiContext.getInstallationContext().getKeyPairClient());
        clientV3.setSessionToken(apiContext.getSessionToken());
        CompletableFuture<READ_MonetaryAccountBank_for_UserEndpoint.Response<?>> responseCompletableFuture =
                clientV3.rEAD_MonetaryAccountBank_for_User(wirespecGetRequest);

        // response mapping
        validateResponseGet(responseCompletableFuture);

        CompletableFuture<CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Response<?>> responseCompletableFuturePost =
                clientV3.cREATE_RequestInquiry_for_User_MonetaryAccount(wirespecPostRequest);

        // response mapping
        validateResponsePost(responseCompletableFuturePost);
    }


    @Test
    void testSomeLevelOfIntermediateMapping3() throws ExecutionException, InterruptedException, TimeoutException {

        var httpClient = HttpClients.createDefault();

        var context = new Context(
                apiContext.getApiKey(),
                "serverName",
                apiContext.getInstallationContext().getPublicKeyServer(),
                apiContext.getInstallationContext().getKeyPairClient(),
                1,
                2,
                apiContext.getSessionToken(),
                apiContext.getSessionContext().getUserId()

        );
        var handler = new WirespecRawRequestHandler("https://public-api.sandbox.bunq.com/v1", httpClient);
        var clientV4 = new MonetaryAccountClientV4(handler, context);

        CompletableFuture<READ_MonetaryAccountBank_for_UserEndpoint.Response<?>> responseCompletableFuture =
                clientV4.rEAD_MonetaryAccountBank_for_User(wirespecGetRequest);

        // response mapping
        validateResponseGet(responseCompletableFuture);

        CompletableFuture<CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Response<?>> responseCompletableFuturePost =
                clientV4.cREATE_RequestInquiry_for_User_MonetaryAccount(wirespecPostRequest);

        // response mapping
        validateResponsePost(responseCompletableFuturePost);
    }

    private static MonetaryAccountBankRead validateResponseGet(CompletableFuture<READ_MonetaryAccountBank_for_UserEndpoint.Response<?>> responseCompletableFuture) throws InterruptedException, ExecutionException, TimeoutException {
        return responseCompletableFuture.thenApply(response -> {
//                    System.out.println(response);
                    switch (response) {
                        case READ_MonetaryAccountBank_for_UserEndpoint.ResponseMonetaryAccountBankRead a200 -> {
                            MonetaryAccountBankRead body = a200.getBody();
                            assertThat(body.balance().isPresent()).isTrue();
                            System.out.println(body.balance().get());
                            return body;
                        }
                        case READ_MonetaryAccountBank_for_UserEndpoint.ResponseREAD_MonetaryAccountBank_for_User400ResponseBody a400 -> {
                            READ_MonetaryAccountBank_for_User400ResponseBody body = a400.getBody();
                            throw new RuntimeException(body.Error().toString());
                        }
                    }
                })
                .exceptionally(e -> {
                    logger.error("Exception happened. No good", e);
                    fail("Exception happened. No good");
                    return null;
                }).get(20_000, TimeUnit.MILLISECONDS);
    }

    private static RequestInquiryCreate validateResponsePost(CompletableFuture<CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Response<?>> responseCompletableFuture) throws InterruptedException, ExecutionException, TimeoutException {
        return responseCompletableFuture.thenApply(response -> {
//                    System.out.println(response);
                    switch (response) {
                        case CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.ResponseRequestInquiryCreate a200 -> {
                            RequestInquiryCreate body = a200.getBody();
                            assertThat(body.Id().orElseThrow().id()).isPresent();
                            System.out.println(body.Id().orElseThrow().id().get());
                            return body;
                        }
                        case CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.ResponseCREATE_RequestInquiry_for_User_MonetaryAccount400ResponseBody a400 -> {
                            var body = a400.getBody();
                            throw new RuntimeException(body.Error().toString());
                        }
                    }
                })
                .exceptionally(e -> {
                    logger.error("Exception happened. No good", e);
                    fail("Exception happened. No good");
                    return null;
                }).get(20_000, TimeUnit.MILLISECONDS);
    }

    private static int getSandboxAccountId() {
        Pagination pagination = new Pagination();
        pagination.setCount(100);

        List<MonetaryAccountBank> allAccount = MonetaryAccountBank.list(pagination.getUrlParamsCountOnly()).getValue();

        return allAccount.stream()
                .findFirst()
                .orElseThrow(() -> new IllegalStateException("There are no active accounts enabled for the current user / session"))
                .getId();
    }

    /**
     * Execute a GET request.
     *
     * @return The raw response of the GET request.
     */
    public BunqResponseRaw getX(
            ApiContext apiContext,
            String uri,
            Map<String, String> params,
            Map<String, String> customHeaders
    ) {
        if (params == null) {
            params = new HashMap<>();
        }

        if (customHeaders == null) {
            customHeaders = new HashMap<>();
        }

        try {
            BunqRequestBuilder requestBuilder = new BunqRequestBuilder()
                    .get()
                    .url(determineFullUri(uri, params));
            Response response = executeRequest(apiContext, requestBuilder, customHeaders, uri);

            return createBunqResponseRaw(response);
        } catch (IOException exception) {
            throw new UncaughtExceptionError(exception);
        }
    }

    private HttpUrl determineFullUri(String path, Map<String, String> params) {
        HttpUrl.Builder urlBuilder = new HttpUrl.Builder()
                .scheme("https")
                .host("public-api.sandbox.bunq.com")
                .addPathSegment("v1")
                .addPathSegments(path);

        SortedMap<String, String> paramsSorted = new TreeMap<>(params);

        for (Map.Entry<String, String> param : paramsSorted.entrySet()) {
            urlBuilder.addQueryParameter(param.getKey(), param.getValue());
        }

        return urlBuilder.build();
    }

    /**
     * Endpoints not requiring active session for the request to succeed.
     */
    private static final String DEVICE_SERVER_URL = "device-server";
    private static final String INSTALLATION_URL = "installation";
    private static final String SESSION_SERVER_URL = "session-server";
    private static final String PAYMENT_SERVICE_PROVIDER_CREDENTIAL_URL = "payment-service-provider-credential";

    private static final List<String> URIS_NOT_REQUIRING_ACTIVE_SESSION = Arrays.asList(
            DEVICE_SERVER_URL,
            INSTALLATION_URL,
            SESSION_SERVER_URL,
            PAYMENT_SERVICE_PROVIDER_CREDENTIAL_URL
    );


    private Response executeRequest(
            ApiContext apiContext,
            BunqRequestBuilder request,
            Map<String, String> customHeaders,
            String uri
    ) throws IOException {
        if (!URIS_NOT_REQUIRING_ACTIVE_SESSION.contains(uri) && apiContext.ensureSessionActive()) {
            BunqContext.updateApiContext(apiContext);
        }

        setHeaders(request, customHeaders);

//        return httpClient.newCall(request.build()).execute();
        return null;
    }

    /**
     *
     */
    private void setHeaders(BunqRequestBuilder requestBuilder, Map<String, String> customHeaders) {
        setDefaultHeaders(requestBuilder);
        setCustomHeaders(requestBuilder, customHeaders);
        setSessionHeaders(requestBuilder);
    }

    /**
     *
     */
    private void setDefaultHeaders(BunqRequestBuilder httpEntity) {
        BunqHeader.CACHE_CONTROL.addTo(httpEntity);
        BunqHeader.USER_AGENT.addTo(httpEntity);
        BunqHeader.LANGUAGE.addTo(httpEntity);
        BunqHeader.REGION.addTo(httpEntity);
        BunqHeader.CLIENT_REQUEST_ID.addTo(httpEntity, UUID.randomUUID().toString());
        BunqHeader.GEOLOCATION.addTo(httpEntity);
    }

    /**
     *
     */
    private void setCustomHeaders(Request.Builder requestBuilder, Map<String, String> customHeaders) {
        for (Map.Entry<String, String> entry : customHeaders.entrySet()) {
            requestBuilder.addHeader(entry.getKey(), entry.getValue());
        }
    }

    /**
     *
     */
    private void setSessionHeaders(BunqRequestBuilder requestBuilder) {
        String sessionToken = apiContext.getSessionToken();

        if (sessionToken != null) {
            BunqHeader.CLIENT_AUTHENTICATION.addTo(requestBuilder, sessionToken);
            BunqHeader.CLIENT_SIGNATURE.addTo(requestBuilder, generateSignature(requestBuilder));
        }
    }

    private String generateSignature(BunqRequestBuilder requestBuilder) {
        return SecurityUtils.generateSignature(requestBuilder,
                apiContext.getInstallationContext().getKeyPairClient());
    }

    private BunqResponseRaw createBunqResponseRaw(Response response)
            throws IOException {
        int responseCode = response.code();
        byte[] responseBodyBytes = Objects.requireNonNull(response.body()).bytes();

        assertResponseSuccess(responseCode, responseBodyBytes, getResponseId(response));
        validateResponseSignature(responseCode, responseBodyBytes, response);

//        return new BunqResponseRaw(responseBodyBytes, getHeadersMap(response));
        return null;
    }

    /**
     *
     */
    private static String getResponseId(Response response) {
        Map<String, String> headerMap = getHeadersMap(response);

        return BunqHeader.CLIENT_RESPONSE_ID.getHeaderValueOrDefault(headerMap);
    }


    private static void assertResponseSuccess(Integer responseCode, byte[] responseBodyBytes, String responseId) {
        if (responseCode == null) {
            responseCode = 0; // DUMMY_RESPONSE_CODE;
        }

        if (!Pattern.matches("2[0-9]{2}", responseCode.toString())) {
            throw createApiExceptionRequestUnsuccessful(responseCode, new String(responseBodyBytes), responseId);
        }
    }

    protected static Map<String, String> getHeadersMap(Response response) {
        HashMap<String, String> headersMap = new HashMap<>();

        for (String headerName : response.headers().names()) {
            headersMap.put(headerName, response.headers().get(headerName));
        }

        return headersMap;
    }


    private static ApiException createApiExceptionRequestUnsuccessful(
            Integer responseCode,
            String responseBody,
            String responseId
    ) {
        List<String> allErrorDescription = new ArrayList<>();

        try {
            allErrorDescription.addAll(fetchAllErrorDescription(responseBody));
        } catch (JsonSyntaxException exception) {
            allErrorDescription.add(responseBody);
        }

        return ExceptionFactory.createExceptionForResponse(responseCode, allErrorDescription, responseId);
    }

    /**
     *
     */
    private static List<String> fetchAllErrorDescription(String responseBody)
            throws JsonSyntaxException {
        List<String> errorDescriptions = new ArrayList<>();
        GsonBuilder gsonBuilder = BunqGsonBuilder.buildDefault();
        JsonObject responseBodyJson = gsonBuilder.create().fromJson(responseBody, JsonObject.class);

        if (responseBodyJson.getAsJsonObject().has(FIELD_ERROR)) {
            errorDescriptions.addAll(fetchAllErrorDescription(responseBodyJson));
        } else {
            errorDescriptions.add(responseBody);
        }

        return errorDescriptions;
    }

    /**
     *
     */
    private static List<String> fetchAllErrorDescription(JsonObject responseBodyJson) {
        List<String> errorDescriptions = new ArrayList<>();
        JsonArray exceptionBodies = responseBodyJson.getAsJsonObject().getAsJsonArray(FIELD_ERROR);

        for (JsonElement exceptionBody : exceptionBodies) {
            JsonObject exceptionBodyJson = exceptionBody.getAsJsonObject();
            errorDescriptions.add(exceptionBodyJson.get(FIELD_ERROR_DESCRIPTION).getAsString());
        }

        return errorDescriptions;
    }


    /**
     *
     */
    private void validateResponseSignature(
            int responseCode,
            byte[] responseBodyBytes,
            Response response
    ) {
        InstallationContext installationContext = apiContext.getInstallationContext();

        if (installationContext != null) {
            SecurityUtils.validateResponseSignature(responseCode, responseBodyBytes, response,
                    installationContext.getPublicKeyServer());
        }
    }


}
