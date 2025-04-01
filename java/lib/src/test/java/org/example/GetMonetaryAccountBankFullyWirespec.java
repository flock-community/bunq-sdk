package org.example;

import community.flock.bunq.java.example.GsonBunqSerializer;
import community.flock.wirespec.generated.java.READ_MonetaryAccountBank_for_UserEndpoint;
import community.flock.wirespec.java.Wirespec;

import java.util.concurrent.CompletableFuture;

public class GetMonetaryAccountBankFullyWirespec implements READ_MonetaryAccountBank_for_UserEndpoint.Handler {
    private final GsonBunqSerializer serialization = new GsonBunqSerializer();

    @Override
    public CompletableFuture<READ_MonetaryAccountBank_for_UserEndpoint.Response<?>> rEAD_MonetaryAccountBank_for_User(READ_MonetaryAccountBank_for_UserEndpoint.Request request) {
        Wirespec.RawRequest rawRequest = READ_MonetaryAccountBank_for_UserEndpoint.Handler.toRequest(serialization, request);

        // do network stuff, fill rawResponse
        CompletableFuture<Wirespec.RawResponse> rawResponse = CompletableFuture.completedFuture(null); // TODO

        CompletableFuture<READ_MonetaryAccountBank_for_UserEndpoint.Response<?>> response = rawResponse
                .thenApply(it -> READ_MonetaryAccountBank_for_UserEndpoint.Handler.fromResponse(serialization, it));
        return response;
    }
}
