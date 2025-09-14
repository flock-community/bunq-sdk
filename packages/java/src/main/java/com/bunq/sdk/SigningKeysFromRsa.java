package com.bunq.sdk;

import java.io.IOException;
import java.security.interfaces.RSAPrivateKey;
import java.security.interfaces.RSAPublicKey;

import static com.bunq.sdk.BunqSigningKeysUtil.validateKeyCompatibility;

public final class SigningKeysFromRsa implements SigningKeys {
    private final RSAPrivateKey privateKey;
    private final RSAPublicKey publicKey;
    private String privateKeyPem;
    private String publicKeyPem;

    public SigningKeysFromRsa(RSAPrivateKey privateKey, RSAPublicKey publicKey) throws IOException {
        this.privateKey = privateKey;
        this.publicKey = publicKey;
        validateKeyCompatibility(privateKey, publicKey);

        this.privateKeyPem = BunqSigningKeysGenerator.convertPrivateKeyToPem(privateKey);
        this.publicKeyPem = BunqSigningKeysGenerator.convertPublicKeyToPem(publicKey);

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
