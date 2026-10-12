package com.bunq.sdk;

import org.bouncycastle.asn1.pkcs.PrivateKeyInfo;
import org.bouncycastle.util.io.pem.PemObject;
import org.bouncycastle.util.io.pem.PemWriter;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.function.Executable;

import java.io.StringWriter;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class SigningKeyValidationTest {
    private final SigningKeys valid = BunqSigningKeysGenerator.generateBunqSigningKeys();

    private static String pem(String type, byte[] der) throws Exception {
        StringWriter out = new StringWriter();
        try (PemWriter writer = new PemWriter(out)) {
            writer.writeObject(new PemObject(type, der));
        }
        return out.toString();
    }

    private static <T extends SigningKeyValidationException> void assertFailure(
            Class<T> type, KeyType keyType, ValidationStage stage, String phrase, Executable block) {
        T e = assertThrows(type, block);
        assertEquals(keyType, e.keyType());
        assertEquals(stage, e.stage());
        assertTrue(e.getMessage().contains(phrase), e.getMessage());
        System.out.println("MESSAGE[" + phrase + "]: " + e.getMessage());
    }

    private byte[] pkcs1Private() throws Exception {
        return PrivateKeyInfo.getInstance(valid.privateKey().getEncoded()).parsePrivateKey().toASN1Primitive().getEncoded();
    }

    @Test
    void pkcs1PrivateKeyGetsOpensslConversionCommand() throws Exception {
        String pkcs1 = pem("RSA PRIVATE KEY", pkcs1Private());
        assertFailure(InvalidPemFormatException.class, KeyType.PRIVATE, ValidationStage.PEM_PARSING,
                "Private key validation failed during PEM parsing: the key is in PKCS#1 format",
                () -> new SigningKeysFromPem(pkcs1, valid.publicKeyPem()));
        assertFailure(InvalidPemFormatException.class, KeyType.PRIVATE, ValidationStage.PEM_PARSING,
                "openssl pkcs8 -topk8 -inform PEM -outform PEM -nocrypt -in private_key.pem -out private_key_pkcs8.pem",
                () -> new SigningKeysFromPem(pkcs1, valid.publicKeyPem()));
    }

    @Test
    void encryptedPrivateKeyIsRejected() throws Exception {
        String encrypted = pem("ENCRYPTED PRIVATE KEY", valid.privateKey().getEncoded());
        assertFailure(InvalidPemFormatException.class, KeyType.PRIVATE, ValidationStage.PEM_PARSING,
                "the command asks for the passphrase", () -> new SigningKeysFromPem(encrypted, valid.publicKeyPem()));
    }

    @Test
    void truncatedPemReportsMissingEndLine() {
        String truncated = valid.privateKeyPem().substring(0, valid.privateKeyPem().indexOf("-----END"));
        assertFailure(InvalidPemFormatException.class, KeyType.PRIVATE, ValidationStage.PEM_PARSING,
                "looks truncated", () -> new SigningKeysFromPem(truncated, valid.publicKeyPem()));
    }

    @Test
    void invalidBase64BodyIsRejected() {
        String bad = "-----BEGIN PUBLIC KEY-----\n!!!not base64!!!\n-----END PUBLIC KEY-----\n";
        assertFailure(InvalidPemFormatException.class, KeyType.PUBLIC, ValidationStage.PEM_PARSING,
                "not valid base64", () -> new SigningKeysFromPem(valid.privateKeyPem(), bad));
    }

    @Test
    void ecPrivateKeyIsRejectedAsNonRsa() throws Exception {
        KeyPairGenerator generator = KeyPairGenerator.getInstance("EC");
        generator.initialize(256);
        KeyPair ec = generator.generateKeyPair();
        String ecPem = pem("PRIVATE KEY", ec.getPrivate().getEncoded());
        assertFailure(InvalidRsaKeyException.class, KeyType.PRIVATE, ValidationStage.RSA_VALIDATION,
                "Private key validation failed during RSA validation", () -> new SigningKeysFromPem(ecPem, valid.publicKeyPem()));
    }

    @Test
    void mismatchedKeyPairIsReportedForBothKeys() {
        SigningKeys other = BunqSigningKeysGenerator.generateBunqSigningKeys();
        assertFailure(KeyMismatchException.class, KeyType.BOTH, ValidationStage.COMPATIBILITY_CHECK,
                "Private and public key validation failed during compatibility check",
                () -> new SigningKeysFromPem(valid.privateKeyPem(), other.publicKeyPem()));
    }

    @Test
    void literalBackslashNIsDetected() {
        String envVar = valid.privateKeyPem().trim().replace("\n", "\\n");
        assertFailure(InvalidPemFormatException.class, KeyType.PRIVATE, ValidationStage.PEM_PARSING,
                "literal \\n sequences", () -> new SigningKeysFromPem(envVar, valid.publicKeyPem()));
    }

    @Test
    void singleLinePemIsDetected() {
        String oneLine = valid.publicKeyPem().trim().replace("\n", " ");
        assertFailure(InvalidPemFormatException.class, KeyType.PUBLIC, ValidationStage.PEM_PARSING,
                "no line breaks", () -> new SigningKeysFromPem(valid.privateKeyPem(), oneLine));
    }

    @Test
    void certificateBeforeTheKeyIsReportedAsWrongBlock() throws Exception {
        String cert = pem("CERTIFICATE", new byte[]{1, 2, 3}) + valid.publicKeyPem();
        assertFailure(InvalidPemFormatException.class, KeyType.PUBLIC, ValidationStage.PEM_PARSING,
                "the first PEM block is 'CERTIFICATE'", () -> new SigningKeysFromPem(valid.privateKeyPem(), cert));
    }

    @Test
    void pkcs1PublicKeyGetsConversionCommand() throws Exception {
        String pkcs1Public = pem("RSA PUBLIC KEY", valid.publicKey().getEncoded());
        assertFailure(InvalidPemFormatException.class, KeyType.PUBLIC, ValidationStage.PEM_PARSING,
                "openssl rsa -RSAPublicKey_in -in public_key.pem -pubout -out public_key_spki.pem",
                () -> new SigningKeysFromPem(valid.privateKeyPem(), pkcs1Public));
    }

    @Test
    void publicKeyPassedAsPrivateKey() {
        assertFailure(InvalidPemFormatException.class, KeyType.PRIVATE, ValidationStage.PEM_PARSING,
                "may be swapped", () -> new SigningKeysFromPem(valid.publicKeyPem(), valid.publicKeyPem()));
    }

    @Test
    void privateKeyPassedAsPublicKey() {
        assertFailure(InvalidPemFormatException.class, KeyType.PUBLIC, ValidationStage.PEM_PARSING,
                "may be swapped", () -> new SigningKeysFromPem(valid.privateKeyPem(), valid.privateKeyPem()));
    }

    @Test
    void crOnlyLineEndingsLoad() {
        new SigningKeysFromPem(valid.privateKeyPem().replace("\n", "\r"), valid.publicKeyPem());
    }

    @Test
    void trailingSpacesLoad() {
        String spaced = String.join("\n", valid.privateKeyPem().lines().map(l -> l + "   ").toList());
        new SigningKeysFromPem(spaced, valid.publicKeyPem());
    }

    @Test
    void indentedPemLoads() {
        String indented = String.join("\n", valid.publicKeyPem().lines().map(l -> "    " + l).toList());
        new SigningKeysFromPem(valid.privateKeyPem(), indented);
    }

    @Test
    void concatenatedPrivateAndPublicPemUsesTheFirstBlock() {
        new SigningKeysFromPem(valid.privateKeyPem() + valid.publicKeyPem(), valid.publicKeyPem());
    }

    @Test
    void droppedBodyLineMentionsTruncatedOrCorrupted() {
        List<String> lines = new ArrayList<>(Arrays.asList(valid.privateKeyPem().split("\n")));
        lines.remove(2);
        assertFailure(InvalidRsaKeyException.class, KeyType.PRIVATE, ValidationStage.RSA_VALIDATION,
                "may be truncated or corrupted", () -> new SigningKeysFromPem(String.join("\n", lines), valid.publicKeyPem()));
    }
}
