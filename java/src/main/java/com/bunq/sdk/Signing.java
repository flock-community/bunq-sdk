package com.bunq.sdk;

import org.bouncycastle.jce.provider.BouncyCastleProvider;
import org.bouncycastle.util.io.pem.PemObject;
import org.bouncycastle.util.io.pem.PemReader;
import org.bouncycastle.util.io.pem.PemWriter;

import java.io.IOException;
import java.io.StringReader;
import java.io.StringWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.security.*;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.PKCS8EncodedKeySpec;
import java.security.spec.X509EncodedKeySpec;
import java.util.Base64;

public class Signing {
    private final Config config;

    public Signing(Config config) {
        this.config = config;
        if (Security.getProvider("BC") == null) {
            Security.addProvider(new BouncyCastleProvider());
        }
    }

    public Pair<String, String> generateRsaKeyPair() {
        try {
            if (config.getPrivateKeyFile().exists() && config.getPublicKeyFile().exists()) {
                String privateKeyPem = Files.readString(config.getPrivateKeyFile().toPath());
                String publicKeyPem = Files.readString(config.getPublicKeyFile().toPath());
                return new Pair<>(privateKeyPem, publicKeyPem);
            }

            KeyPairGenerator keyPairGenerator = KeyPairGenerator.getInstance("RSA", "BC");
            keyPairGenerator.initialize(2048, new SecureRandom());
            KeyPair keyPair = keyPairGenerator.generateKeyPair();

            String privateKeyPem = convertPrivateKeyToPem(keyPair.getPrivate());
            String publicKeyPem = convertPublicKeyToPem(keyPair.getPublic());

            Files.writeString(config.getPrivateKeyFile().toPath(), privateKeyPem);
            Files.writeString(config.getPublicKeyFile().toPath(), publicKeyPem);

            System.out.println("bunq - creating new keypair [KEEP THESE FILES SAFE]");
            return new Pair<>(privateKeyPem, publicKeyPem);
        } catch (Exception e) {
            throw new RuntimeException("Failed to generate RSA key pair", e);
        }
    }

    private String convertPrivateKeyToPem(PrivateKey privateKey) throws IOException {
        StringWriter stringWriter = new StringWriter();
        try (PemWriter pemWriter = new PemWriter(stringWriter)) {
            pemWriter.writeObject(new PemObject("PRIVATE KEY", privateKey.getEncoded()));
        }
        return stringWriter.toString();
    }

    private String convertPublicKeyToPem(PublicKey publicKey) throws IOException {
        StringWriter stringWriter = new StringWriter();
        try (PemWriter pemWriter = new PemWriter(stringWriter)) {
            pemWriter.writeObject(new PemObject("PUBLIC KEY", publicKey.getEncoded()));
        }
        return stringWriter.toString();
    }

    private PrivateKey loadPrivateKey() throws IOException, NoSuchAlgorithmException, InvalidKeySpecException, NoSuchProviderException {
        String privateKeyPem = Files.readString(config.getPrivateKeyFile().toPath());
        KeyFactory keyFactory = KeyFactory.getInstance("RSA", "BC");
        PemObject pemContent = new PemReader(new StringReader(privateKeyPem)).readPemObject();
        PKCS8EncodedKeySpec keySpec = new PKCS8EncodedKeySpec(pemContent.getContent());
        return keyFactory.generatePrivate(keySpec);
    }

    private PublicKey loadPublicKey() throws IOException, NoSuchAlgorithmException, InvalidKeySpecException, NoSuchProviderException {
        String publicKeyPem = Files.readString(config.getPublicKeyFile().toPath());
        KeyFactory keyFactory = KeyFactory.getInstance("RSA", "BC");
        PemObject pemContent = new PemReader(new StringReader(publicKeyPem)).readPemObject();
        X509EncodedKeySpec keySpec = new X509EncodedKeySpec(pemContent.getContent());
        return keyFactory.generatePublic(keySpec);
    }

    public String signData(String data) {
        try {
            PrivateKey privateKey = loadPrivateKey();
            // Ensure the data is encoded in UTF-8 exactly as it will be sent
            byte[] encodedData = data.getBytes(StandardCharsets.UTF_8);

            // Generate signature using SHA256 and PKCS#1 v1.5 padding
            Signature signature = Signature.getInstance("SHA256withRSA");
            signature.initSign(privateKey);
            signature.update(encodedData);
            byte[] signatureBytes = signature.sign();

            // Encode in Base64
            return Base64.getEncoder().encodeToString(signatureBytes);
        } catch (Exception e) {
            throw new RuntimeException("Failed to sign data", e);
        }
    }

    public boolean verifyResponse(String responseBody, String signature) {
        try {
            PublicKey publicKey = loadPublicKey();
            byte[] decodedSignature = Base64.getDecoder().decode(signature);

            Signature verifier = Signature.getInstance("SHA256withRSA", "BC");
            verifier.initVerify(publicKey);
            verifier.update(responseBody.getBytes(StandardCharsets.UTF_8));

            return verifier.verify(decodedSignature);
        } catch (Exception e) {
            System.out.println("[ERROR] Signature verification failed: " + e.getMessage());
            return false;
        }
    }

    // Simple Pair class since Java doesn't have a built-in Pair class
    public static class Pair<A, B> {
        private final A first;
        private final B second;

        public Pair(A first, B second) {
            this.first = first;
            this.second = second;
        }

        public A getFirst() {
            return first;
        }

        public B getSecond() {
            return second;
        }
    }
}