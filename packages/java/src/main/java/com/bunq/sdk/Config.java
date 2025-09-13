package com.bunq.sdk;

import org.bouncycastle.jce.provider.BouncyCastleProvider;
import org.bouncycastle.util.io.pem.PemObject;
import org.bouncycastle.util.io.pem.PemReader;

import java.io.StringReader;
import java.security.KeyFactory;
import java.security.Security;
import java.security.interfaces.RSAPrivateKey;
import java.security.interfaces.RSAPublicKey;
import java.security.spec.PKCS8EncodedKeySpec;
import java.security.spec.X509EncodedKeySpec;
import java.util.Objects;

/**
 * Configuration class for bunq API client containing all necessary settings and credentials
 * for establishing and managing API connections.
 *
 * All parameters are validated upon construction to ensure proper format and compatibility.
 */
public record Config(
        String serviceName,
        String apiKey,
        String privateKeyPem,
        String publicKeyPem,
        RSAPrivateKey privateKey,
        RSAPublicKey publicKey,
        String userAgent,
        String cacheControl,
        String language,
        String region,
        String clientRequestId,
        String geolocation
) {
    private static final long EXPECTED_RSA_EXPONENT = 65537L;

    /**
     * Validates the configuration and loads RSA keys for validation.
     * Throws ConfigValidationException if validation fails.
     */
    public Config {
        validateBasicParameters(serviceName, apiKey);
    }

    public Config(String serviceName, String apiKey, String privateKeyPem, String publicKeyPem) {
        this(
                serviceName,
                apiKey,
                privateKeyPem,
                publicKeyPem,
                validateAndLoadPrivateKey(privateKeyPem),
                validateAndLoadPublicKey(publicKeyPem),
                null,
                null,
                null,
                null,
                null,
                null
        );

        validateKeyCompatibility(privateKey, publicKey);
    }


    private static void validateBasicParameters(String serviceName, String apiKey) {
        if (serviceName == null || serviceName.isBlank()) {
            throw new IllegalArgumentException("Service name cannot be blank");
        }
        if (apiKey == null || apiKey.isBlank()) {
            throw new IllegalArgumentException("API key cannot be blank");
        }
    }

    private static RSAPrivateKey validateAndLoadPrivateKey(String privateKeyPem) {
        try {
            if (!privateKeyPem.contains("-----BEGIN PRIVATE KEY-----") ||
                !privateKeyPem.contains("-----END PRIVATE KEY-----")) {
                throw new InvalidPemFormatException("Private key must be in PKCS#8 PEM format");
            }

            ensureBouncyCastleProvider();
            var keyFactory = KeyFactory.getInstance("RSA", "BC");
            
            try (var pemReader = new PemReader(new StringReader(privateKeyPem))) {
                PemObject pemContent = pemReader.readPemObject();
                if (pemContent == null) {
                    throw new InvalidPemFormatException("Could not parse private key PEM content");
                }
                
                var keySpec = new PKCS8EncodedKeySpec(pemContent.getContent());
                var privateKey = keyFactory.generatePrivate(keySpec);
                
                if (!(privateKey instanceof RSAPrivateKey rsaPrivateKey)) {
                    throw new InvalidRsaKeyException("Private key must be an RSA key");
                }
                
                return rsaPrivateKey;
            }
        } catch (ConfigValidationException e) {
            throw e;
        } catch (Exception e) {
            throw new InvalidRsaKeyException("Failed to load private key: " + e.getMessage(), e);
        }
    }

    private static RSAPublicKey validateAndLoadPublicKey(String publicKeyPem) {
        try {
            if (!publicKeyPem.contains("-----BEGIN PUBLIC KEY-----") ||
                !publicKeyPem.contains("-----END PUBLIC KEY-----")) {
                throw new InvalidPemFormatException("Public key must be in X.509 PEM format");
            }

            ensureBouncyCastleProvider();
            var keyFactory = KeyFactory.getInstance("RSA", "BC");
            
            try (var pemReader = new PemReader(new StringReader(publicKeyPem))) {
                PemObject pemContent = pemReader.readPemObject();
                if (pemContent == null) {
                    throw new InvalidPemFormatException("Could not parse public key PEM content");
                }
                
                var keySpec = new X509EncodedKeySpec(pemContent.getContent());
                var publicKey = keyFactory.generatePublic(keySpec);
                
                if (!(publicKey instanceof RSAPublicKey rsaPublicKey)) {
                    throw new InvalidRsaKeyException("Public key must be an RSA key");
                }
                
                return rsaPublicKey;
            }
        } catch (ConfigValidationException e) {
            throw e;
        } catch (Exception e) {
            throw new InvalidRsaKeyException("Failed to load public key: " + e.getMessage(), e);
        }
    }

    private static void validateKeyCompatibility(RSAPrivateKey privateKey, RSAPublicKey publicKey) {
        try {
            // Verify that the private and public keys are a matching pair
            // by checking that they have the same modulus
            if (!Objects.equals(privateKey.getModulus(), publicKey.getModulus())) {
                throw new KeyMismatchException("Private and public keys do not form a valid key pair (modulus mismatch)");
            }
            
            // Additional check: verify that the public exponent matches the expected value for RSA
            if (publicKey.getPublicExponent().longValue() != EXPECTED_RSA_EXPONENT) {
                throw new InvalidRsaKeyException(
                    "Public key has unexpected exponent. Expected " + EXPECTED_RSA_EXPONENT + 
                    ", got " + publicKey.getPublicExponent()
                );
            }
        } catch (ConfigValidationException e) {
            throw e;
        } catch (Exception e) {
            throw new KeyMismatchException("Failed to validate key compatibility: " + e.getMessage());
        }
    }

    private static void ensureBouncyCastleProvider() {
        if (Security.getProvider("BC") == null) {
            Security.addProvider(new BouncyCastleProvider());
        }
    }
}
