package com.bunq.sdk;

import com.bunq.sdk.generated.endpoint.List_all_MonetaryAccountBank_for_User;
import com.bunq.sdk.generated.endpoint.READ_User;
import community.flock.wirespec.java.Wirespec;

import java.lang.reflect.Method;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.CompletableFuture;

import static com.bunq.sdk.WirespecBase.send;
import static com.bunq.sdk.WirespecBase.serialization;


public class Client implements List_all_MonetaryAccountBank_for_User.Handler, READ_User.Handler {
    private final Signing signing;
    private final Context context;

    public Client(Signing signing, Context context) {
        this.signing = signing;
        this.context = context;
    }

    @Override
    public CompletableFuture<List_all_MonetaryAccountBank_for_User.Response<?>> list_all_MonetaryAccountBank_for_User(
            List_all_MonetaryAccountBank_for_User.Request request) {
        return handle(signing, context, request);
    }

    @Override
    public CompletableFuture<READ_User.Response<?>> rEAD_User(READ_User.Request request) {
        return handle(signing, context, request);
    }

    @SuppressWarnings("unchecked")
    public static <Req extends Wirespec.Request<?>, Res extends Wirespec.Response<?>> CompletableFuture<Res> handle(
            Signing signing, Context context, Req request) {
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
            Method toMethod = client.getClass().getMethod("to", Wirespec.Request.class);
            toMethod.setAccessible(true);

            // Invoke the to method to get the raw request
            Wirespec.RawRequest rawRequest = (Wirespec.RawRequest) toMethod.invoke(client, request);

            // Add the authentication header
            Map<String, java.util.List<String>> headers = new HashMap<>(rawRequest.headers());
            headers.put("X-Bunq-Client-Authentication", java.util.List.of(context.getSessionToken()));

            // Create a new raw request with the updated headers
            Wirespec.RawRequest reqToken = new Wirespec.RawRequest(
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
                            Method fromMethod = client.getClass().getMethod("from", Wirespec.RawResponse.class);
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
    }
}