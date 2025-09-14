package com.bunq.sdk;

import java.security.interfaces.RSAPrivateKey;
import java.security.interfaces.RSAPublicKey;

import static com.bunq.sdk.BunqSigningKeysUtil.validateKeyCompatibility;

public final class SigningKeysFromPem implements SigningKeys {
    private final String privateKeyPem;
    private final String publicKeyPem;
    private final RSAPrivateKey privateKey;
    private final RSAPublicKey publicKey;

    public SigningKeysFromPem(String privateKeyPem, String publicKeyPem) {
        this.privateKeyPem = privateKeyPem;
        this.publicKeyPem = publicKeyPem;
        this.privateKey = BunqSigningKeysUtil.validateAndLoadPrivateKey(privateKeyPem);
        this.publicKey = BunqSigningKeysUtil.validateAndLoadPublicKey(publicKeyPem);
        validateKeyCompatibility(privateKey, publicKey);
    }

    @Override
    public String publicKeyPem() {
        return publicKeyPem;
    }

    @Override
    public String privateKeyPem() {
        return privateKeyPem;
    }

    @Override
    public RSAPrivateKey privateKey() {
        return privateKey;
    }

    @Override
    public RSAPublicKey publicKey() {
        return publicKey;
    }
}
