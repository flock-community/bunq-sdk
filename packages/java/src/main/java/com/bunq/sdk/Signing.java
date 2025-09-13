package com.bunq.sdk;

import java.nio.charset.StandardCharsets;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.security.Signature;
import java.util.Base64;

public class Signing {


    public static String signData(Config config, String data) {
        try {
            PrivateKey privateKey = config.privateKey();
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

    public static boolean verifyResponse(Config config, String responseBody, String signature) {
        try {
            PublicKey publicKey = config.publicKey();
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

}
