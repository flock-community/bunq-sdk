package com.bunq.sdk;

import java.io.File;

public record Config(
        String serviceName,
        String apiKey,
        File privateKeyFile,
        File publicKeyFile,
        String userAgent,
        String cacheControl,
        String language,
        String region,
        String clientRequestId,
        String geolocation
) {
    public Config(String serviceName, String apiKey,  File privateKeyFile, File publicKeyFile) {
        this(
                serviceName,
                apiKey,
                privateKeyFile,
                publicKeyFile,
                null,
                null,
                null,
                null,
                null,
                null
        );
    }

    public Config(String serviceName, String apiKey) {
        this(
                serviceName,
                apiKey,
                new File("../private_key.pem"),
                new File("../public_key.pem"),
                null,
                null,
                null,
                null,
                null,
                null
        );
    }
}
