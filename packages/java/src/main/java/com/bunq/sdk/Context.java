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
import com.bunq.sdk.generated.model.UserApiKey;
import com.bunq.sdk.generated.model.UserApiKeyAnchoredUser;
import com.bunq.sdk.generated.model.UserCompany;
import com.bunq.sdk.generated.model.UserPaymentServiceProvider;
import com.bunq.sdk.generated.model.UserPerson;
import community.flock.wirespec.java.Wirespec.RawRequest;
import org.jetbrains.annotations.NotNull;

import java.time.Instant;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;
import java.util.function.Supplier;

import static com.bunq.sdk.Wirespec.send;
import static com.bunq.sdk.Wirespec.serialization;


public record Context(
        String serverPublicKey,
        long deviceId,
        long sessionId,
        String sessionToken,
        long userId,
        Instant sessionExpiryTime,
        String installationToken,
        Config config
) {

    public static Context initContext(Config config) {

        try {
            InstallationCreate installation = createInstallation(config).get();
            var installationToken = Optional.ofNullable(installation.Token())
                    .flatMap(it -> it)
                    .flatMap(InstallationToken::token).orElseThrow(error("Token not available"));

            DeviceServerCreate deviceServer = createDeviceServer(config, installationToken).get();
            SessionServerCreate serverSession = createSessionServer(config, installationToken).get();

            Long sessionTimeoutSeconds = getSessionTimeout(serverSession)
                    .orElseGet(() -> {
                        System.out.println("bunq - No session timeout found in session server response, using default of 30 minutes");
                        return 30 * 60L;
                    });
            Instant sessionExpiryTime = Instant.now().plusSeconds(sessionTimeoutSeconds);

            return new Context(
                    installation.ServerPublicKey().flatMap(InstallationServerPublicKey::server_public_key).orElseThrow(error("No server public key")),
                    deviceServer.Id().flatMap(DeviceServerCreateId::id).orElseThrow(error("No device id")),
                    serverSession.Id().flatMap(BunqId::id).orElseThrow(error("No session id")),
                    serverSession.Token().flatMap(SessionServerToken::token).orElseThrow(error("No session token")),
                    getUserId(serverSession),
                    sessionExpiryTime,
                    installationToken,
                    config);

        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    /**
     * Refresh this context's session.
     * This recreates the session with the same device and installation but gets a new session token.
     *
     * @return A new Context with refreshed session information
     */
    public Context refreshSession() {
        if (installationToken == null) {
            throw new IllegalStateException("Cannot refresh session: no installation token available in context");
        }

        try {
            SessionServerCreate serverSession = createSessionServer(config, installationToken).get();

            Long sessionTimeoutSeconds = getSessionTimeout(serverSession)
                    .orElseGet(() -> {
                        System.out.println("bunq - No session timeout found in session server response, using default of 30 minutes");
                        return 30 * 60L;
                    });
            Instant sessionExpiryTime = Instant.now().plusSeconds(sessionTimeoutSeconds);

            return new Context(
                    this.serverPublicKey,
                    this.deviceId,
                    serverSession.Id().flatMap(BunqId::id).orElseThrow(error("No session id")),
                    serverSession.Token().flatMap(SessionServerToken::token).orElseThrow(error("No session token")),
                    getUserId(serverSession),
                    sessionExpiryTime,
                    this.installationToken,
                    this.config
            );
        } catch (Exception e) {
            throw new RuntimeException("Failed to refresh session", e);
        }
    }


    private static @NotNull Supplier<RuntimeException> error(String message) {
        return () -> new IllegalStateException(message);
    }

    private static CompletableFuture<InstallationCreate> createInstallation(Config config) {
        Installation body = new Installation(config.signingKeys().publicKeyPem());

        CREATE_Installation.Request request = new CREATE_Installation.Request(body);

        RawRequest rawRequest = CREATE_Installation.Handler.toRequest(serialization, request);
        return send(config, rawRequest).thenApply(rawResponse -> {
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

    private static CompletableFuture<DeviceServerCreate> createDeviceServer(Config config, String token) {
        DeviceServer body = new DeviceServer(config.serviceName(), config.apiKey(), Optional.of(Collections.singletonList("*")));

        CREATE_DeviceServer.Request request = new CREATE_DeviceServer.Request(body);

        var rawRequest = CREATE_DeviceServer.Handler.toRequest(serialization, request);
        var authRequest = new RawRequest(
                rawRequest.method(),
                rawRequest.path(),
                rawRequest.queries(),
                Map.of("X-Bunq-Client-Authentication", List.of(token)),
                rawRequest.body()
        );
        return send(config, authRequest).thenApply(rawResponse -> {
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

    private static CompletableFuture<SessionServerCreate> createSessionServer(Config config, String token) {
        SessionServer body = new SessionServer(config.apiKey());

        CREATE_SessionServer.Request request = new CREATE_SessionServer.Request(body);
        RawRequest rawRequest = CREATE_SessionServer.Handler.toRequest(serialization, request);
        var authRequest = new RawRequest(
                rawRequest.method(),
                rawRequest.path(),
                rawRequest.queries(),
                Map.of(
                        "UserAgent", List.of(config.serviceName()),
                        "X-Bunq-Client-Authentication", List.of(token)
                ),
                rawRequest.body()
        );
        return send(config, authRequest).thenApply(rawResponse -> {
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

    /**
     * Sessions can be for various types of users, of which only one is filled.
     */
    private static long getUserId(SessionServerCreate sessionServer) {
        return sessionServer.UserPerson().flatMap(UserPerson::id)
                .or(() -> sessionServer.UserCompany().flatMap(UserCompany::id))
                .or(() -> sessionServer.UserApiKey().flatMap(UserApiKey::id))
                .or(() -> sessionServer.UserPaymentServiceProvider().flatMap(UserPaymentServiceProvider::id))
                .orElseThrow(() -> new IllegalStateException("No user id found in the SessionServerCreate response"));
    }

    /**
     * Extract session timeout from the user in the SessionServerCreate response.
     */
    private static Optional<Long> getSessionTimeout(SessionServerCreate sessionServer) {
        return sessionServer.UserPerson().flatMap(UserPerson::session_timeout)
                .or(() -> sessionServer.UserCompany().flatMap(UserCompany::session_timeout))
                .or(() -> sessionServer.UserPaymentServiceProvider().flatMap(UserPaymentServiceProvider::session_timeout))
                .or(() -> sessionServer.UserApiKey().flatMap(Context::getUserApiKeySessionTimeout));
    }

    private static Optional<Long> getUserApiKeySessionTimeout(UserApiKey userApiKey) {
        return userApiKey.granted_by_user().flatMap(Context::getUserApiKeyAnchoredUserSessionTimeout)
                .or(() -> userApiKey.requested_by_user().flatMap(Context::getUserApiKeyAnchoredUserSessionTimeout));
    }

    private static Optional<Long> getUserApiKeyAnchoredUserSessionTimeout(UserApiKeyAnchoredUser anchoredUser) {
        return anchoredUser.UserPerson().flatMap(UserPerson::session_timeout)
                .or(() -> anchoredUser.UserCompany().flatMap(UserCompany::session_timeout))
                .or(() -> anchoredUser.UserPaymentServiceProvider().flatMap(UserPaymentServiceProvider::session_timeout));
    }

    @Override
    public @NotNull String toString() {
        return "Context{" + "serverPublicKey='" + serverPublicKey + '\'' + ", deviceId=" + deviceId + ", sessionId=" + sessionId + ", sessionToken='" + sessionToken + '\'' + ", userId=" + userId + ", config=" + config + '}';
    }
}
