package com.bunq.sdk;

import org.bouncycastle.util.io.pem.PemObject;
import org.bouncycastle.util.io.pem.PemWriter;

import java.io.IOException;
import java.io.StringWriter;
import java.security.KeyPairGenerator;
import java.security.NoSuchAlgorithmException;
import java.security.NoSuchProviderException;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.security.SecureRandom;

public class RsaKeyPairGenerator {

    private static final KeyPairGenerator keyPairGenerator;

    static {
        try {
            keyPairGenerator = KeyPairGenerator.getInstance("RSA", "BC");
        } catch (NoSuchAlgorithmException | NoSuchProviderException e) {
            throw new RuntimeException(e);
        }

        keyPairGenerator.initialize(2048, new SecureRandom());
    }

    /**
     * Generates a new RSA key pair and returns the PEM strings.
     * This is now a static utility method since Config validation handles key loading.
     */
    public static KeyPair<String, String> generateRsaKeyPair() {
        try {
            java.security.KeyPair keyPair = keyPairGenerator.generateKeyPair();

            String privateKeyPem = convertPrivateKeyToPem(keyPair.getPrivate());
            String publicKeyPem = convertPublicKeyToPem(keyPair.getPublic());

            System.out.println("bunq - created new keypair [KEEP THESE SAFE]");
            return new KeyPair<>(privateKeyPem, publicKeyPem);
        } catch (Exception e) {
            throw new RuntimeException("Failed to generate RSA key pair", e);
        }
    }

    private static String convertPrivateKeyToPem(PrivateKey privateKey) throws IOException {
        StringWriter stringWriter = new StringWriter();
        try (PemWriter pemWriter = new PemWriter(stringWriter)) {
            pemWriter.writeObject(new PemObject("PRIVATE KEY", privateKey.getEncoded()));
        }
        return stringWriter.toString();
    }

    private static String convertPublicKeyToPem(PublicKey publicKey) throws IOException {
        StringWriter stringWriter = new StringWriter();
        try (PemWriter pemWriter = new PemWriter(stringWriter)) {
            pemWriter.writeObject(new PemObject("PUBLIC KEY", publicKey.getEncoded()));
        }
        return stringWriter.toString();
    }

    // Simple Pair class since Java doesn't have a built-in Pair class
    public record KeyPair<A, B>(A privateKey, B publicKey) {
    }
}
