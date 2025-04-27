package com.bunq.sdk;

import com.bunq.sdk.generated.endpoint.CREATE_DeviceServer;
import com.bunq.sdk.generated.endpoint.CREATE_Installation;
import com.bunq.sdk.generated.endpoint.CREATE_SessionServer;
import com.bunq.sdk.generated.model.BunqId;
import com.bunq.sdk.generated.model.DeviceServer;
import com.bunq.sdk.generated.model.DeviceServerCreate;
import com.bunq.sdk.generated.model.DeviceServerCreateId;
import com.bunq.sdk.generated.model.Installation;
import com.bunq.sdk.generated.model.InstallationCreate;
import com.bunq.sdk.generated.model.InstallationServerPublicKey;
import com.bunq.sdk.generated.model.InstallationToken;
import com.bunq.sdk.generated.model.SessionServer;
import com.bunq.sdk.generated.model.SessionServerCreate;
import com.bunq.sdk.generated.model.SessionServerToken;
import com.bunq.sdk.generated.model.UserPerson;
import community.flock.wirespec.java.Wirespec.RawRequest;
import org.jetbrains.annotations.NotNull;

import java.util.Collections;
import java.util.Objects;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.function.Supplier;

import static com.bunq.sdk.WirespecBase.send;
import static com.bunq.sdk.WirespecBase.serialization;


public class Context {
    private final String apiKey;
    private final String serviceName;
    private final String serverPublicKey;
    private final long deviceId;
    private final long sessionId;
    private final String sessionToken;
    private final long userId;

    public Context(String apiKey, String serviceName, String serverPublicKey, long deviceId, long sessionId, String sessionToken, long userId) {
        this.apiKey = apiKey;
        this.serviceName = serviceName;
        this.serverPublicKey = serverPublicKey;
        this.deviceId = deviceId;
        this.sessionId = sessionId;
        this.sessionToken = sessionToken;
        this.userId = userId;
    }

    public String getApiKey() {
        return apiKey;
    }

    public String getServiceName() {
        return serviceName;
    }

    public String getServerPublicKey() {
        return serverPublicKey;
    }

    public long getDeviceId() {
        return deviceId;
    }

    public long getSessionId() {
        return sessionId;
    }

    public String getSessionToken() {
        return sessionToken;
    }

    public long getUserId() {
        return userId;
    }

    public static Context initContext(Config config) throws ExecutionException, InterruptedException {
        Signing signing = new Signing(config);

        InstallationCreate installation = createInstallation(signing, config.getServiceName(), signing.generateRsaKeyPair().getSecond()).get();
        var installationToken = Optional.ofNullable(installation.Token()).flatMap(it -> it).flatMap(InstallationToken::token).orElseThrow(error("Token not available"));


        DeviceServerCreate deviceServer = createDeviceServer(signing, config.getServiceName(), config.getApiKey(), installationToken).get();
        SessionServerCreate serverSession = createSessionServer(signing, config.getServiceName(), config.getApiKey(), installationToken).get();

        return new Context(config.getApiKey(), config.getServiceName(), installation.ServerPublicKey().flatMap(InstallationServerPublicKey::server_public_key).orElseThrow(error("No server public key")), deviceServer.Id().flatMap(DeviceServerCreateId::id).orElseThrow(error("No device id")), serverSession.Id().flatMap(BunqId::id).orElseThrow(error("No session id")), serverSession.Token().flatMap(SessionServerToken::token).orElseThrow(error("No session token")), serverSession.UserPerson().flatMap(UserPerson::id).orElseThrow(error("No user id")));
    }

    private static <T> T throwRuntimeException(String message) {
        throw error(message).get();
    }

    private static @NotNull Supplier<RuntimeException> error(String message) {
        return () -> new IllegalStateException(message);
    }

    private static CompletableFuture<InstallationCreate> createInstallation(Signing signing, String serviceName, String publicKeyPem) {
        Installation body = new Installation(publicKeyPem);

        CREATE_Installation.Request request = new CREATE_Installation.Request(Optional.empty(), serviceName, Optional.empty(), Optional.empty(), Optional.empty(), Optional.empty(), "", body);

        RawRequest rawRequest = CREATE_Installation.Handler.toRequest(serialization, request);
        return send(signing, rawRequest).thenApply(rawResponse -> {
            Object response = CREATE_Installation.Handler.fromResponse(serialization, rawResponse);
            if (response instanceof CREATE_Installation.Response200) {
                return ((CREATE_Installation.Response200) response).getBody();
            } else if (response instanceof CREATE_Installation.Response400) {
                throw new RuntimeException("Cannot create installation");
            } else {
                throw new RuntimeException("Unexpected response type: " + response.getClass().getName());
            }
        });
    }

    private static CompletableFuture<DeviceServerCreate> createDeviceServer(Signing signing, String serviceName, String apiKey, String token) {
        DeviceServer body = new DeviceServer(serviceName, apiKey, Optional.of(Collections.singletonList("*")));

        CREATE_DeviceServer.Request request = new CREATE_DeviceServer.Request(Optional.empty(), serviceName, Optional.empty(), Optional.empty(), Optional.empty(), Optional.empty(), token, body);

        RawRequest rawRequest = CREATE_DeviceServer.Handler.toRequest(serialization, request);
        return send(signing, rawRequest).thenApply(rawResponse -> {

            Object response = CREATE_DeviceServer.Handler.fromResponse(serialization, rawResponse);

            if (response instanceof CREATE_DeviceServer.Response200) {
                return ((CREATE_DeviceServer.Response200) response).getBody();
            } else if (response instanceof CREATE_DeviceServer.Response400) {
                throw new RuntimeException("Cannot create device server");
            } else {
                throw new RuntimeException("Unexpected response type: " + response.getClass().getName());
            }
        });
    }

    private static CompletableFuture<SessionServerCreate> createSessionServer(Signing signing, String serviceName, String apiKey, String token) {
        SessionServer body = new SessionServer(apiKey);

        CREATE_SessionServer.Request request = new CREATE_SessionServer.Request(Optional.empty(), serviceName, Optional.empty(), Optional.empty(), Optional.empty(), Optional.empty(), token, body

        );

        RawRequest rawRequest = CREATE_SessionServer.Handler.toRequest(serialization, request);
        return send(signing, rawRequest).thenApply(rawResponse -> {

            Object response = CREATE_SessionServer.Handler.fromResponse(serialization, rawResponse);

            if (response instanceof CREATE_SessionServer.Response200) {
                return ((CREATE_SessionServer.Response200) response).getBody();
            } else if (response instanceof CREATE_SessionServer.Response400) {
                throw new RuntimeException("Cannot create session server");
            } else {
                throw new RuntimeException("Unexpected response type: " + response.getClass().getName());
            }
        });
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Context context = (Context) o;
        return deviceId == context.deviceId && sessionId == context.sessionId && userId == context.userId && Objects.equals(apiKey, context.apiKey) && Objects.equals(serviceName, context.serviceName) && Objects.equals(serverPublicKey, context.serverPublicKey) && Objects.equals(sessionToken, context.sessionToken);
    }

    @Override
    public int hashCode() {
        return Objects.hash(apiKey, serviceName, serverPublicKey, deviceId, sessionId, sessionToken, userId);
    }

    @Override
    public String toString() {
        return "Context{" + "apiKey='" + apiKey + '\'' + ", serviceName='" + serviceName + '\'' + ", serverPublicKey='" + serverPublicKey + '\'' + ", deviceId=" + deviceId + ", sessionId=" + sessionId + ", sessionToken='" + sessionToken + '\'' + ", userId=" + userId + '}';
    }
}