package com.bunq.sdk;

import org.junit.jupiter.api.Test;

import java.io.File;
import java.nio.file.Files;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class BunqSigningKeysGeneratorTest {

    @Test
    void testGenerateKeyPair() throws Exception {
        var signingKeys = BunqSigningKeysGenerator.generateBunqSigningKeys();

        assertEquals("RSA", signingKeys.privateKey().getAlgorithm());
        assertEquals("RSA", signingKeys.publicKey().getAlgorithm());
        assertTrue(signingKeys.privateKey().getEncoded().length > 0);
        assertTrue(signingKeys.publicKey().getEncoded().length > 0);
        assertEquals("PKCS#8", signingKeys.privateKey().getFormat());
        assertEquals("X.509", signingKeys.publicKey().getFormat());
        assertTrue(signingKeys.privateKey().getEncoded().length > 1024);
        assertTrue(signingKeys.privateKey().getModulus().bitLength() >= 2048);
        assertTrue(signingKeys.privateKey().getPrivateExponent().longValue() != 65537L);
        assertEquals(signingKeys.privateKey().getModulus().bitLength(), signingKeys.publicKey().getModulus().bitLength());
        assertEquals(65537L, signingKeys.publicKey().getPublicExponent().longValue());

        assertTrue(signingKeys.publicKeyPem().startsWith("-----BEGIN PUBLIC KEY-----"));
        assertTrue(signingKeys.publicKeyPem().endsWith("-----END PUBLIC KEY-----\n"));

        assertTrue(signingKeys.privateKeyPem().startsWith("-----BEGIN PRIVATE KEY-----"));
        assertTrue(signingKeys.privateKeyPem().endsWith("-----END PRIVATE KEY-----\n"));
    }

    @Test
    void testGenerateKeyPairAndWritePemFiles() throws Exception {
        File publicKeyFile = new File("../../public_key.pem");
        File privateKeyFile = new File("../../private_key.pem");
        publicKeyFile.deleteOnExit();
        privateKeyFile.deleteOnExit();

        var signingKeys = BunqSigningKeysGenerator.generateBunqSigningKeys(privateKeyFile, publicKeyFile);

        String publicKeyString = Files.readString(publicKeyFile.toPath());
        String privateKeyString = Files.readString(privateKeyFile.toPath());

        assertEquals(signingKeys.privateKeyPem(), privateKeyString);
        assertEquals(signingKeys.publicKeyPem(), publicKeyString);

        assertTrue(publicKeyString.startsWith("-----BEGIN PUBLIC KEY-----"));
        assertTrue(publicKeyString.endsWith("-----END PUBLIC KEY-----\n"));
    }
}