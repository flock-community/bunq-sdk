package flock.community.bunq_sdk.java;

import com.bunq.sdk.context.ApiContext;
import com.bunq.sdk.context.BunqContext;
import com.bunq.sdk.exception.BunqException;
import com.bunq.sdk.model.generated.endpoint.RequestInquiry;
import com.bunq.sdk.model.generated.endpoint.SandboxUserPerson;
import com.bunq.sdk.model.generated.object.Amount;
import com.bunq.sdk.model.generated.object.Pointer;
import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.stream.JsonReader;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.io.StringReader;
import java.util.UUID;

import static com.bunq.sdk.context.ApiEnvironmentType.SANDBOX;
import static com.bunq.sdk.http.BunqHeader.*;

/**
 * Bunq sandbox specifics
 * <p>
 * Copy/pasted and adapted from <a href="https://github.com/bunq/tinker_java">Bunq's tinker project </a>
 */
public final class BunqSandboxRepositoryHelper {
    private static final Logger log = LoggerFactory.getLogger(BunqSandboxRepositoryHelper.class);

    /**
     * Error constants.
     */
    private static final String ERROR_COULD_NOT_GENERATE_NEW_API_KEY = "Encountered error while retrieving new sandbox ApiKey.\nError message %s";

    /**
     * Field constants.
     */
    private static final String FIELD_RESPONSE = "Response";
    private static final String FIELD_API_KEY = "ApiKey";

    /**
     *
     */
    private static final String POINTER_TYPE_EMAIL = "EMAIL";
    private static final String CURRENCY_EUR = "EUR";
    private static final String DEVICE_SERVER_DESCRIPTION = "Teambalance SANDBOX app";

    /**
     * The index of the fist item in an array.
     */
    private static final int INDEX_FIRST = 0;

    /**
     * Http constants.
     */
    private static final int HTTP_STATUS_OK = 200;

    /**
     * Request spending money constants.
     */
    private static final String REQUEST_SPENDING_MONEY_AMOUNT = "500.0";
    private static final String REQUEST_SPENDING_MONEY_RECIPIENT = "sugardaddy@bunq.com";
    private static final String REQUEST_SPENDING_MONEY_DESCRIPTION = "Requesting some spending money.";
    private static final int REQUEST_SPENDING_MONEY_WAIT_TIME_MILLISECONDS = 1000;

    /**
     * Balance constant.
     */
    private static final double BALANCE_ZERO = 0.0;


    private BunqSandboxRepositoryHelper() {
        // utility class
    }

    public static ApiContext createSandboxApiContext() {
        SandboxUserPerson sandboxUser = generateNewSandboxUser();
        return ApiContext.create(SANDBOX, sandboxUser.getApiKey(), DEVICE_SERVER_DESCRIPTION);
    }

    public static void requestSpendingMoneyIfNeeded() {
        if (shouldRequestSpendingMoney()) {
            RequestInquiry.create(
                    new Amount(REQUEST_SPENDING_MONEY_AMOUNT, CURRENCY_EUR),
                    new Pointer(POINTER_TYPE_EMAIL, REQUEST_SPENDING_MONEY_RECIPIENT),
                    REQUEST_SPENDING_MONEY_DESCRIPTION,
                    false
            );

            try {
                Thread.sleep(REQUEST_SPENDING_MONEY_WAIT_TIME_MILLISECONDS);
            } catch (InterruptedException exception) {
                Thread.currentThread().interrupt();
                log.warn(exception.getMessage());
            }
        }
    }

    private static SandboxUserPerson generateNewSandboxUser() {
        OkHttpClient client = new OkHttpClient();

        Request request = new Request.Builder()
                .url("https://%s/%s/sandbox-user-person".formatted(SANDBOX.getBaseUri(), SANDBOX.getApiVersion()))
                .post(RequestBody.create(null, new byte[INDEX_FIRST]))
                .addHeader(CLIENT_REQUEST_ID.getHeaderName(), UUID.randomUUID().toString())
                .addHeader(CACHE_CONTROL.getHeaderName(), CACHE_CONTROL.getDefaultValue())
                .addHeader(GEOLOCATION.getHeaderName(), GEOLOCATION.getDefaultValue())
                .addHeader(LANGUAGE.getHeaderName(), LANGUAGE.getDefaultValue())
                .addHeader(REGION.getHeaderName(), REGION.getDefaultValue())
                .build();

        try {
            try (Response response = client.newCall(request).execute()) {
                if (response.code() == HTTP_STATUS_OK) {
                    String responseString = response.body().string();
                    JsonObject jsonObject = new Gson().fromJson(responseString, JsonObject.class);
                    JsonObject apiKey = jsonObject.getAsJsonArray(FIELD_RESPONSE).get(INDEX_FIRST).getAsJsonObject().get(FIELD_API_KEY).getAsJsonObject();

                    return SandboxUserPerson.fromJsonReader(new JsonReader(new StringReader(apiKey.toString())));
                } else {
                    throw new BunqException(ERROR_COULD_NOT_GENERATE_NEW_API_KEY.formatted(response.body().string()));
                }
            }
        } catch (IOException e) {
            throw new BunqException(e.getMessage());
        }
    }

    private static boolean shouldRequestSpendingMoney() {
        return (Double.parseDouble(BunqContext.getUserContext().getPrimaryMonetaryAccountBank().getBalance().getValue())
                <= BALANCE_ZERO);
    }
}
