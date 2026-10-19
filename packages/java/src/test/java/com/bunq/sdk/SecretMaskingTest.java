package com.bunq.sdk;

import org.junit.jupiter.api.Test;

import java.time.Instant;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class SecretMaskingTest {

    @Test
    void toStringMasksSecretsAndKeepsNonSecretFields() {
        SigningKeys keys = BunqSigningKeysGenerator.generateBunqSigningKeys();
        Config config = new Config(BunqServer.BUNQ_SANDBOX_SERVER, "my-service", "secret-api-key", keys,
                null, null, null, null, null, null);
        Context context = new Context("server-key", 1, 2, "secret-session", 3, Instant.EPOCH, "secret-install", config);

        String text = context.toString();

        for (String secret : List.of("secret-api-key", "secret-session", "secret-install",
                keys.privateKeyPem().lines().toList().get(1))) {
            assertFalse(text.contains(secret), secret);
        }
        assertTrue(text.contains("my-service"));
        assertTrue(text.contains("userId=3"));
    }
}
