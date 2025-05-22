package com.bunq.sdk;

import java.io.File;
import java.util.Objects;

public class Config {
    private final String serviceName;
    private final String apiKey;
    private final File privateKeyFile;
    private final File publicKeyFile;

    public Config(String serviceName, String apiKey, File privateKeyFile, File publicKeyFile) {
        this.serviceName = serviceName;
        this.apiKey = apiKey;
        this.privateKeyFile = privateKeyFile;
        this.publicKeyFile = publicKeyFile;
    }

    public Config(String serviceName, String apiKey) {
        this(serviceName, apiKey, new File("../private_key.pem"), new File("../public_key.pem"));
    }

    public String getServiceName() {
        return serviceName;
    }

    public String getApiKey() {
        return apiKey;
    }

    public File getPrivateKeyFile() {
        return privateKeyFile;
    }

    public File getPublicKeyFile() {
        return publicKeyFile;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Config config = (Config) o;
        return Objects.equals(serviceName, config.serviceName) &&
                Objects.equals(apiKey, config.apiKey) &&
                Objects.equals(privateKeyFile, config.privateKeyFile) &&
                Objects.equals(publicKeyFile, config.publicKeyFile);
    }

    @Override
    public int hashCode() {
        return Objects.hash(serviceName, apiKey, privateKeyFile, publicKeyFile);
    }

    @Override
    public String toString() {
        return "Config{" +
                "serviceName='" + serviceName + '\'' +
                ", apiKey='" + apiKey + '\'' +
                ", privateKeyFile=" + privateKeyFile +
                ", publicKeyFile=" + publicKeyFile +
                '}';
    }
}