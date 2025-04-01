package community.flock.bunq.java;


import com.bunq.sdk.security.SecurityUtils;
import community.flock.bunq.java.context.InstallationContext;
import community.flock.wirespec.generated.java.CREATE_DeviceServerEndpoint;
import community.flock.wirespec.generated.java.CREATE_InstallationEndpoint;
import community.flock.wirespec.generated.java.DeviceServer;
import community.flock.wirespec.generated.java.Installation;

import java.security.KeyPair;
import java.security.PublicKey;
import java.util.HashMap;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;

/**
 * API context
 *
 * @param apiKey
 * @param serverName
 * @param serverPublicKey
 * @param keyPair
 * @param deviceId
 * @param sessionId
 * @param sessionToken
 * @param userId
 */
public record Context(
        String apiKey,
        String serverName,
        PublicKey serverPublicKey,
        KeyPair keyPair,
        int deviceId,
        int sessionId,
        String sessionToken,
        int userId
) {
}

public class ContextX {
    private final String apiKey;
    private final String serverName;
    private PublicKey serverPublicKey;
    private KeyPair keyPair;
    private final int deviceId;
    private final int sessionId;
    private String sessionToken;
    private final int userId;

    public ContextX(String apiKey,
                    String deviceDescription,
                    List<String> permittedIps,
                    String proxy) {
        this.apiKey = apiKey;
        this.serverName = deviceDescription;

        initialize(deviceDescription, permittedIps);


    }

    public ContextX create(String apiKey, String deviceDescription,
                           List<String> permittedIps, ContextInitializerHandler requestHandler) {
        String xBunqClientAuthentication = "bunq-client-authd";
        Installation body = new Installation("client-public-key");

        String userAgent = "Hallo from Flock bunq sdk";
        var responseCompletableFuture = requestHandler.cREATE_Installation(new CREATE_InstallationEndpoint.Request(
                        Optional.empty(),
                        userAgent,
                        Optional.empty(),
                        Optional.empty(),
                        Optional.empty(),
                        Optional.empty(),
                        xBunqClientAuthentication,
                        body

                )).thenApply(it ->
                        switch (it) {
                            case CREATE_InstallationEndpoint.ResponseCREATE_Installation400ResponseBody responseCREATEInstallation400ResponseBody ->
                                    null;
                            case CREATE_InstallationEndpoint.ResponseInstallationCreate responseInstallationCreate ->
                                    throw new RuntimeException("Whoopsie");
                        }
                )
                .thenApply(it -> {

                            DeviceServer deviceServer = new DeviceServer(
                                    "description",
                                    "secret",
                                    Optional.of(List.of(permittedIps.toArray(new String[0])))
                            );
                            return requestHandler.cREATE_DeviceServer(new CREATE_DeviceServerEndpoint.Request(
                                    Optional.empty(),
                                    userAgent,
                                    Optional.empty(),
                                    Optional.empty(),
                                    Optional.empty(),
                                    Optional.empty(),
                                    xBunqClientAuthentication,
                                    deviceServer

                            ));
                        }

                ).thenApply(it ->
                        null
                        );


        var responseCompletableFuture2 = requestHandler.cREATE_SessionServer(null/*TODO */);
    }

    private void initialize(String deviceDescription, List<String> permittedIps) {
        /* The calls below are order-sensitive: to initialize a Device Registration, we need an
         * Installation, and to initialize a Session we need a Device Registration. */
        initializeInstallation();
        initializeDeviceRegistration(deviceDescription, permittedIps);
        initializeSession();
    }

    /**
     * Create a new installation and store its data in an InstallationContext.
     */
    private void initializeInstallation() {
        this.keyPair = SecurityUtils.generateKeyPair();

        var publicKeyClientString = SecurityUtils.getPublicKeyFormattedString(this.keyPair.getPublic());
        this.sessionToken = installation.getSessionToken().getToken();
        this.serverPublicKey = SecurityUtils.createPublicKeyFromFormattedString(installation.getPublicKeyServer());
        this.serverPublicKey = installation.getPublicKeyServer();
        installationContext = new InstallationContext(installation, keyPairClient);
    }

    private static byte[] generateRequestBodyBytes(String publicKeyClientString) {
        HashMap<String, Object> installationRequestBody = new HashMap<>();
        installationRequestBody.put(FIELD_CLIENT_PUBLIC_KEY, publicKeyClientString);

        return gson.toJson(installationRequestBody).getBytes();
    }
}