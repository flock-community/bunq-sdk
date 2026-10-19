package com.bunq.sdk;

import com.bunq.sdk.generated.endpoint.CreateDeviceServer;
import com.bunq.sdk.generated.endpoint.CreateInstallation;
import com.bunq.sdk.generated.endpoint.CreateSessionServer;
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

            String serverPublicKey = installation.ServerPublicKey().flatMap(InstallationServerPublicKey::server_public_key).orElseThrow(error("No server public key"));
            DeviceServerCreate deviceServer = createDeviceServer(config, installationToken, serverPublicKey).get();
            SessionServerCreate serverSession = createSessionServer(config, installationToken, serverPublicKey).get();

            Long sessionTimeoutSeconds = getSessionTimeout(serverSession)
                    .orElseGet(() -> {
                        System.out.println("bunq - No session timeout found in session server response, using default of 30 minutes");
                        return 30 * 60L;
                    });
            Instant sessionExpiryTime = Instant.now().plusSeconds(sessionTimeoutSeconds);

            return new Context(
                    serverPublicKey,
                    deviceServer.Id().flatMap(DeviceServerCreateId::id).orElseThrow(error("No device id")),
                    serverSession.Id().flatMap(BunqId::id).orElseThrow(error("No session id")),
                    serverSession.Token().flatMap(SessionServerToken::token).orElseThrow(error("No session token")),
                    getUserId(serverSession),
                    sessionExpiryTime,
                    installationToken,
                    config);

        } catch (Exception e) {
            if (e instanceof InterruptedException) {
                Thread.currentThread().interrupt();
            }
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
            SessionServerCreate serverSession = createSessionServer(config, installationToken, this.serverPublicKey).get();

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
            if (e instanceof InterruptedException) {
                Thread.currentThread().interrupt();
            }
            throw new RuntimeException("Failed to refresh session", e);
        }
    }


    private static @NotNull Supplier<RuntimeException> error(String message) {
        return () -> new IllegalStateException(message);
    }

    private static String setupFailure(String action, Optional<String> description) {
        return "Cannot " + action + " (status 400): " + description.orElse(null);
    }

    private static CompletableFuture<InstallationCreate> createInstallation(Config config) {
        Installation body = new Installation(config.signingKeys().publicKeyPem());

        CreateInstallation.Request request = new CreateInstallation.Request(body);

        RawRequest rawRequest = CreateInstallation.toRawRequest(serialization, request);
        return send(config, rawRequest).thenApply(Wirespec::requireTyped).thenApply(rawResponse -> {
            Object response = CreateInstallation.fromRawResponse(serialization, rawResponse);
            if (response instanceof CreateInstallation.Response200) {
                return ((CreateInstallation.Response200) response).body();
            } else if (response instanceof CreateInstallation.Response400 error) {
                throw new RuntimeException(setupFailure("create installation",
                        error.body().Error().flatMap(errors -> errors.stream().findFirst()).flatMap(e -> e.error_description())));
            } else {
                throw new RuntimeException("Unexpected response type: " + response.getClass().getName());
            }
        });
    }

    private static CompletableFuture<DeviceServerCreate> createDeviceServer(Config config, String token, String serverPublicKey) {
        DeviceServer body = new DeviceServer(config.serviceName(), config.apiKey(), Optional.of(Collections.singletonList("*")));

        CreateDeviceServer.Request request = new CreateDeviceServer.Request(body);

        var rawRequest = CreateDeviceServer.toRawRequest(serialization, request);
        var authRequest = new RawRequest(
                rawRequest.method(),
                rawRequest.path(),
                rawRequest.queries(),
                Map.of("X-Bunq-Client-Authentication", List.of(token)),
                rawRequest.body()
        );
        return send(config, authRequest).thenApply(response -> Wirespec.requireSigned(response, serverPublicKey)).thenApply(rawResponse -> {
            Object response = CreateDeviceServer.fromRawResponse(serialization, rawResponse);
            if (response instanceof CreateDeviceServer.Response200) {
                return ((CreateDeviceServer.Response200) response).body();
            } else if (response instanceof CreateDeviceServer.Response400 error) {
                throw new RuntimeException(setupFailure("create device server",
                        error.body().Error().flatMap(errors -> errors.stream().findFirst()).flatMap(e -> e.error_description())));
            } else {
                throw new RuntimeException("Unexpected response type: " + response.getClass().getName());
            }
        });
    }

    private static CompletableFuture<SessionServerCreate> createSessionServer(Config config, String token, String serverPublicKey) {
        SessionServer body = new SessionServer(config.apiKey());

        CreateSessionServer.Request request = new CreateSessionServer.Request(body);
        RawRequest rawRequest = CreateSessionServer.toRawRequest(serialization, request);
        var authRequest = new RawRequest(
                rawRequest.method(),
                rawRequest.path(),
                rawRequest.queries(),
                Map.of(
                        "X-Bunq-Client-Authentication", List.of(token)
                ),
                rawRequest.body()
        );
        return send(config, authRequest).thenApply(response -> Wirespec.requireSigned(response, serverPublicKey)).thenApply(rawResponse -> {
            Object response = CreateSessionServer.fromRawResponse(serialization, rawResponse);
            if (response instanceof CreateSessionServer.Response200) {
                return ((CreateSessionServer.Response200) response).body();
            } else if (response instanceof CreateSessionServer.Response400 error) {
                throw new RuntimeException(setupFailure("create session server",
                        error.body().Error().flatMap(errors -> errors.stream().findFirst()).flatMap(e -> e.error_description())));
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
        return "Context{" + "serverPublicKey='" + serverPublicKey + '\'' + ", deviceId=" + deviceId + ", sessionId=" + sessionId + ", sessionToken=***" + ", userId=" + userId + ", sessionExpiryTime=" + sessionExpiryTime + ", installationToken=***" + ", config=" + config + '}';
    }
}
