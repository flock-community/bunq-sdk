package com.bunq.sdk;

import java.io.File;

public record Config(String serviceName, String apiKey, File privateKeyFile, File publicKeyFile) {
    public Config(String serviceName, String apiKey) {
        this(serviceName, apiKey, new File("../private_key.pem"), new File("../public_key.pem"));
    }
}
