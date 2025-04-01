package community.flock.bunq.java.example;

import community.flock.bunq.java.Context;
import community.flock.wirespec.generated.java.CREATE_RequestInquiry_for_User_MonetaryAccount400ResponseBody;
import community.flock.wirespec.generated.java.CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint;
import community.flock.wirespec.generated.java.ErrorArray;
import community.flock.wirespec.generated.java.READ_MonetaryAccountBank_for_User400ResponseBody;
import community.flock.wirespec.generated.java.READ_MonetaryAccountBank_for_UserEndpoint;
import community.flock.wirespec.java.Wirespec;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;

import static java.util.Optional.empty;

public class MonetaryAccountClientV4 implements READ_MonetaryAccountBank_for_UserEndpoint.Handler, CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Handler {
    private static final Logger logger = LoggerFactory.getLogger(MonetaryAccountClientV4.class);
    private final GsonBunqSerializer serialization = new GsonBunqSerializer();
    private final Context context;
    private final WirespecRawRequestHandler handler;

    public MonetaryAccountClientV4(WirespecRawRequestHandler handler, Context context) {
        this.handler = handler;
        this.context = context;
    }

    @Override
    public CompletableFuture<READ_MonetaryAccountBank_for_UserEndpoint.Response<?>> rEAD_MonetaryAccountBank_for_User(READ_MonetaryAccountBank_for_UserEndpoint.Request request) {
        Wirespec.RawRequest rawRequest = READ_MonetaryAccountBank_for_UserEndpoint.Handler.toRequest(serialization, request);
        return CompletableFuture.<READ_MonetaryAccountBank_for_UserEndpoint.Response<?>>supplyAsync(() -> {
                    try {
                        Wirespec.RawResponse response = handler.handle(context, rawRequest, "MonetaryAccountBank");
                        READ_MonetaryAccountBank_for_UserEndpoint.Response<?> typedResponse = READ_MonetaryAccountBank_for_UserEndpoint.Handler.fromResponse(serialization, response);
//                        System.out.println(typedResponse);
                        return typedResponse;
                    } catch (IOException e) {
                        throw new RuntimeException("Could not call bunq", e);
                    }
                })
                .exceptionally(it -> {
                    logger.error("Something went wrong fetching MonetaryAccountBank with", it);
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
            Wirespec.RawRequest rawRequest = CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Handler.toRequest(serialization, request);
            return CompletableFuture.<CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Response<?>>supplyAsync(() -> {
                        try {
                            Wirespec.RawResponse rawResponse = handler.handle(context, rawRequest, null);
                            CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Response<?> typedResponse = CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Handler.fromResponse(serialization, rawResponse);
                            return typedResponse;
                        } catch (IOException e) {
                            throw new RuntimeException(e);
                        }
                    })
                    .exceptionally(it -> {
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
                                        empty()
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
                                        empty()
                                )
                        )
                )
        );
    }
}
