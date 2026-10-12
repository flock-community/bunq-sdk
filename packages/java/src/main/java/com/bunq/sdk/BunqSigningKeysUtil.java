package com.bunq.sdk;

import org.bouncycastle.jce.provider.BouncyCastleProvider;
import org.bouncycastle.util.io.pem.PemHeader;
import org.bouncycastle.util.io.pem.PemObject;
import org.bouncycastle.util.io.pem.PemReader;

import java.io.StringReader;
import java.math.BigInteger;
import java.security.KeyFactory;
import java.security.Security;
import java.security.interfaces.RSAPrivateKey;
import java.security.interfaces.RSAPublicKey;
import java.security.spec.PKCS8EncodedKeySpec;
import java.security.spec.X509EncodedKeySpec;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

class BunqSigningKeysUtil {
    private static final BigInteger EXPECTED_RSA_EXPONENT = BigInteger.valueOf(65537);
    private static final String PKCS8_FIX =
            "openssl pkcs8 -topk8 -inform PEM -outform PEM -nocrypt -in private_key.pem -out private_key_pkcs8.pem";
    private static final String PUBLIC_FROM_PRIVATE_FIX =
            "openssl rsa -in private_key_pkcs8.pem -pubout -out public_key.pem";

    static RSAPrivateKey validateAndLoadPrivateKey(String privateKeyPem) {
        byte[] der = readPemBody(privateKeyPem, "PRIVATE KEY", KeyType.PRIVATE);
        try {
            ensureBouncyCastleProvider();
            return (RSAPrivateKey) KeyFactory.getInstance("RSA", "BC").generatePrivate(new PKCS8EncodedKeySpec(der));
        } catch (Exception e) {
            throw new InvalidRsaKeyException(
                    "not a valid RSA key (" + e.getMessage() + "). The key may be truncated or corrupted, or not an RSA key " +
                            "(only RSA keys are supported). Generate one with: openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048",
                    KeyType.PRIVATE, e);
        }
    }

    static RSAPublicKey validateAndLoadPublicKey(String publicKeyPem) {
        byte[] der = readPemBody(publicKeyPem, "PUBLIC KEY", KeyType.PUBLIC);
        try {
            ensureBouncyCastleProvider();
            return (RSAPublicKey) KeyFactory.getInstance("RSA", "BC").generatePublic(new X509EncodedKeySpec(der));
        } catch (Exception e) {
            throw new InvalidRsaKeyException(
                    "not a valid RSA key (" + e.getMessage() + "). The key may be truncated or corrupted, or not an RSA key " +
                            "(only RSA keys are supported). Derive it with: " + PUBLIC_FROM_PRIVATE_FIX,
                    KeyType.PUBLIC, e);
        }
    }

    private static byte[] readPemBody(String pem, String label, KeyType keyType) {
        if (pem.contains("\\n")) {
            throw invalid("the PEM contains literal \\n sequences; replace them with real newlines", keyType, null);
        }
        List<String> lines = pem.lines().map(String::trim).filter(l -> !l.isEmpty()).collect(Collectors.toList());
        if (lines.size() < 2) {
            throw invalid("the PEM has no line breaks; put the BEGIN line, the base64 body and the END line on separate lines", keyType, null);
        }
        int beginIndex = IntStream.range(0, lines.size())
                .filter(i -> lines.get(i).startsWith("-----BEGIN ") && lines.get(i).endsWith("-----")).findFirst().orElse(-1);
        if (beginIndex >= 0) {
            String endLine = "-----END " + lines.get(beginIndex).substring("-----BEGIN ".length());
            if (lines.subList(beginIndex + 1, lines.size()).stream().noneMatch(endLine::equals)) {
                throw invalid("the '-----END " + label + "-----' line is missing, the PEM looks truncated", keyType, null);
            }
        }

        PemObject block;
        try {
            block = new PemReader(new StringReader(String.join("\n", lines))).readPemObject();
        } catch (Exception e) {
            throw invalid("the body is not valid base64 or is malformed (" + e.getMessage() + "). Re-export the key without modifying it.", keyType, e);
        }
        if (block == null) {
            throw invalid("no PEM block could be read; check that the BEGIN line is present and the line breaks are real newlines", keyType, null);
        }

        String type = block.getType();
        boolean encrypted = type.equals("ENCRYPTED PRIVATE KEY") || block.getHeaders().stream()
                .anyMatch(h -> ((PemHeader) h).getName().equals("Proc-Type") && ((PemHeader) h).getValue().contains("ENCRYPTED"));
        boolean expectsPrivate = keyType == KeyType.PRIVATE;
        if (type.equals(label) && !encrypted) {
            return block.getContent();
        } else if (encrypted && expectsPrivate) {
            throw invalid("the key is encrypted, which is not supported. Decrypt it first (the command asks for the passphrase): " +
                    "openssl pkcs8 -topk8 -nocrypt -in encrypted_key.pem -out private_key_pkcs8.pem", keyType, null);
        } else if (type.equals("RSA PRIVATE KEY") && expectsPrivate) {
            throw invalid("the key is in PKCS#1 format but PKCS#8 ('-----BEGIN PRIVATE KEY-----') is required. Convert it with: " + PKCS8_FIX, keyType, null);
        } else if (type.equals("RSA PUBLIC KEY") && !expectsPrivate) {
            throw invalid("the key is in PKCS#1 format but X.509 ('-----BEGIN PUBLIC KEY-----') is required. Convert it with: " +
                    "openssl rsa -RSAPublicKey_in -in public_key.pem -pubout -out public_key_spki.pem", keyType, null);
        } else if (expectsPrivate && type.endsWith("PUBLIC KEY")) {
            throw invalid("this is a public key, a private key is expected. The keys may be swapped.", keyType, null);
        } else if (!expectsPrivate && type.endsWith("PRIVATE KEY")) {
            throw invalid("this is a private key, a public key is expected. The keys may be swapped. " +
                    "Derive the public key with: " + PUBLIC_FROM_PRIVATE_FIX, keyType, null);
        }
        throw invalid("the first PEM block is '" + type + "' but '" + label + "' is expected", keyType, null);
    }

    private static InvalidPemFormatException invalid(String detail, KeyType keyType, Throwable cause) {
        return new InvalidPemFormatException(detail, keyType, cause);
    }

    static void validateKeyCompatibility(RSAPrivateKey privateKey, RSAPublicKey publicKey) {
        if (!EXPECTED_RSA_EXPONENT.equals(publicKey.getPublicExponent())) {
            throw new InvalidRsaKeyException(
                    "unexpected public exponent. Expected " + EXPECTED_RSA_EXPONENT + ", got " + publicKey.getPublicExponent(),
                    KeyType.PUBLIC);
        }
        if (!privateKey.getModulus().equals(publicKey.getModulus())) {
            throw new KeyMismatchException(
                    "the keys do not form a pair (the moduli differ). Derive the public key with: " + PUBLIC_FROM_PRIVATE_FIX);
        }
    }

    private static void ensureBouncyCastleProvider() {
        if (Security.getProvider("BC") == null) {
            Security.addProvider(new BouncyCastleProvider());
        }
    }
}
