package com.bunq.sdk;

import org.junit.jupiter.api.Test;

import java.io.File;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class SigningTest {

    @Test
    public void testSigning() {
        File privateKeyFile = new File("../../test/private_key.pem");
        File publicKeyFile = new File("../../test/public_key.pem");

        Config config = new Config(
                "",
                "",
                privateKeyFile,
                publicKeyFile
        );

        Signing signing = new Signing(config);
        signing.generateRsaKeyPair();
        String result = signing.signData("Hello");

        assertEquals(
                "fR0Gyn8VfC8eCwq10x5eYAcxXh4nv6331hWAAr77l72zfFScbw3hFSE6iBNklCYc0mfnKezsuRo3re+fTNNHO1oZhfhjc9i4UYxTxBiOEslHrKx9NkXkBZh2RALx/LnhlpyMwB5BBOlFlNeR9Hyj5E8c/a2pObBZRmrZ3cgAnoWF8hhY5Y9XwLS2WIodYIPSQXuQMXyi1UBxhxAbniZ5m1uRSt8gaPmQGMCQtUzvZ8KUXtSvugGPsXHwh94EccZCfjS0sdIQK8AcZ8t5YL6bqkqJ7eVzbxoX6U1nOZVy3MxQMKQ/PFS297er6qsVsGwKbNfaTUvymEb46mM/gQdQDQ==",
                result
        );
    }
}