package com.bunq.sdk;

import org.bouncycastle.jce.provider.BouncyCastleProvider;
import org.bouncycastle.util.io.pem.PemObject;
import org.bouncycastle.util.io.pem.PemWriter;

import java.io.File;
import java.io.IOException;
import java.io.StringWriter;
import java.nio.file.Files;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.NoSuchAlgorithmException;
import java.security.NoSuchProviderException;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.security.SecureRandom;
import java.security.Security;
import java.security.interfaces.RSAPrivateKey;
import java.security.interfaces.RSAPublicKey;

public class BunqSigningKeysGenerator {

    private static final KeyPairGenerator keyPairGenerator;

    static {
        if (Security.getProvider("BC") == null) {
            Security.addProvider(new BouncyCastleProvider());
        }

        try {
            keyPairGenerator = KeyPairGenerator.getInstance("RSA", "BC");
            keyPairGenerator.initialize(2048, new SecureRandom());
        } catch (NoSuchAlgorithmException | NoSuchProviderException e) {
            throw new RuntimeException(e);
        }
    }

    /**
     * Generates a new RSA key pair and returns the PEM strings.
     * This is now a static utility method since Config validation handles key loading.
     */
    public static SigningKeys generateBunqSigningKeys() {
        try {
            KeyPair keyPair = keyPairGenerator.generateKeyPair();
            System.out.println("bunq - created new keypair [KEEP THESE SAFE]");
            return new SigningKeysFromRsa((RSAPrivateKey) keyPair.getPrivate(), (RSAPublicKey) keyPair.getPublic());
        } catch (Exception e) {
            throw new RuntimeException("Failed to generate RSA key pair", e);
        }
    }

    /**
     * Generates and stores an RSA key pair in the specified files. If the files already exist,
     * the existing key pair will be reused. The key pair is generated using a 2048-bit key size.
     *
     * @param privateKeyFile The file where the generated private key will be stored or retrieved from if it already exists.
     * @param publicKeyFile  The file where the generated public key will be stored or retrieved from if it already exists.
     */
    public static SigningKeys generateBunqSigningKeys(File privateKeyFile, File publicKeyFile) {
        try {
            if (privateKeyFile.exists() && publicKeyFile.exists()) {
                String privateKeyPem = Files.readString(privateKeyFile.toPath());
                String publicKeyPem = Files.readString(publicKeyFile.toPath());
                return new SigningKeysFromPem(privateKeyPem, publicKeyPem);
            }

            KeyPairGenerator keyPairGenerator = KeyPairGenerator.getInstance("RSA", "BC");
            keyPairGenerator.initialize(2048, new SecureRandom());
            java.security.KeyPair keyPair = keyPairGenerator.generateKeyPair();

            String privateKeyPem = convertPrivateKeyToPem(keyPair.getPrivate());
            String publicKeyPem = convertPublicKeyToPem(keyPair.getPublic());

            Files.writeString(privateKeyFile.toPath(), privateKeyPem);
            Files.writeString(publicKeyFile.toPath(), publicKeyPem);

            System.out.println("bunq - creating new keypair [KEEP THESE FILES SAFE]");
            return new SigningKeysFromPem(privateKeyPem, publicKeyPem);
        } catch (Exception e) {
            throw new RuntimeException("Failed to generate RSA key pair", e);
        }
    }


    static String convertPrivateKeyToPem(PrivateKey privateKey) throws IOException {
        StringWriter stringWriter = new StringWriter();
        try (PemWriter pemWriter = new PemWriter(stringWriter)) {
            pemWriter.writeObject(new PemObject("PRIVATE KEY", privateKey.getEncoded()));
        }
        return stringWriter.toString();
    }

    static String convertPublicKeyToPem(PublicKey publicKey) throws IOException {
        StringWriter stringWriter = new StringWriter();
        try (PemWriter pemWriter = new PemWriter(stringWriter)) {
            pemWriter.writeObject(new PemObject("PUBLIC KEY", publicKey.getEncoded()));
        }
        return stringWriter.toString();
    }

}

