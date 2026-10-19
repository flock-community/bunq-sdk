package com.bunq.sdk;

import java.nio.charset.StandardCharsets;
import java.security.PrivateKey;
import java.security.Signature;
import java.util.Base64;

public class Signing {


    public static String signData(Config config, String data) {
        try {
            PrivateKey privateKey = config.signingKeys().privateKey();
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

    /** Verifies bunq's {@code X-Bunq-Server-Signature}: SHA256withRSA over the raw response body bytes. */
    public static boolean verifyResponse(String serverPublicKeyPem, byte[] responseBody, String signature) {
        try {
            byte[] decodedSignature = Base64.getDecoder().decode(signature);

            Signature verifier = Signature.getInstance("SHA256withRSA", "BC");
            verifier.initVerify(BunqSigningKeysUtil.validateAndLoadPublicKey(serverPublicKeyPem));
            verifier.update(responseBody);

            return verifier.verify(decodedSignature);
        } catch (Exception e) {
            System.out.println("[ERROR] Signature verification failed: " + e.getMessage());
            return false;
        }
    }

}
