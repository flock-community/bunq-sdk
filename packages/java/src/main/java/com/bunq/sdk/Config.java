package com.bunq.sdk;

import java.io.IOException;
import java.security.interfaces.RSAPrivateKey;
import java.security.interfaces.RSAPublicKey;

/**
 * Configuration class for bunq API client containing all necessary settings and credentials
 * for establishing and managing API connections.
 * <p>
 * All parameters are validated upon construction to ensure proper format and compatibility.
 */
public record Config(
        /** The bunq API server environment to connect to */
        BunqServer bunqServer,
        /** Name of the service/application using this SDK */
        String serviceName,
        /** API key for authentication with bunq servers */
        String apiKey,
        /** Key pair for server-side request signing */
        SigningKeys signingKeys,
        /** Custom User-Agent header value */
        String userAgent,
        /** Cache-Control header value for API requests */
        String cacheControl,
        /** Preferred language for API responses */
        String language,
        /** Geographic region for API requests */
        String region,
        /** Custom client request ID for tracking */
        String clientRequestId,
        /** Geographic location information */
        String geolocation
) {


    /**
     * Validates the configuration and loads RSA keys for validation.
     * Throws ConfigValidationException if validation fails.
     */
    public Config {
        validateBasicParameters(serviceName, apiKey);
    }

    /**
     * Constructor with explicit BunqServer specification
     */
    public Config(BunqServer bunqServer, String serviceName, String apiKey, String privateKeyPem, String publicKeyPem) {
        this(
                bunqServer,
                serviceName,
                apiKey,
                new SigningKeysFromPem(privateKeyPem, publicKeyPem),
                null,
                null,
                null,
                null,
                null,
                null
        );

    }
    /**
     * Constructor with explicit BunqServer specification
     */
    public Config(BunqServer bunqServer, String serviceName, String apiKey, RSAPrivateKey privateKey, RSAPublicKey publicKey) throws IOException {
        this(
                bunqServer,
                serviceName,
                apiKey,
                new SigningKeysFromRsa(privateKey,publicKey),
                null,
                null,
                null,
                null,
                null,
                null
        );

    }



    private static void validateBasicParameters(String serviceName, String apiKey) {
        if (serviceName == null || serviceName.isBlank()) {
            throw new IllegalArgumentException("Service name cannot be blank");
        }
        if (apiKey == null || apiKey.isBlank()) {
            throw new IllegalArgumentException("API key cannot be blank");
        }
    }
}
