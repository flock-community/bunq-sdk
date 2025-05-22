package com.bunq.sdk;

import org.junit.jupiter.api.Test;

import java.io.File;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class SigningTest {

    @Test
    public void testSigning() {
        File privateKeyFile = new File("../../private_key.pem");
        File publicKeyFile = new File("../../public_key.pem");

        Config config = new Config(
                "",
                "",
                privateKeyFile,
                publicKeyFile
        );

        Signing signing = new Signing(config);
        String result = signing.signData("Hello");

        assertEquals(
                "T/jCqiFSe1nj9keIq2Cdg5MISs69IIJa1BcmsQ+0iLTuKWNrbOcSS7lvEF7HSWiW8i7Vu4ofhTaw+iob75UB9qVpy8gZBd6UMSWKNUMDXtqj0LbUcov191m6eYLEme9hkg4R/5L9eEaTGvMuuEjxJ05/GgJe2wj2hhun1WoKGBaNCV9y7UrT6CXODMl45AprtttCpB5smjaCtfnW6NaIijHRanKjjIKLu7XaxYVuEFEYvsgm+aQKdKa1gi90qT48zt/R8MNLqoOH1P4NHAXXnplTh5j1BJEDKk1QMsZBS71KhbQU3y3dRjjf/+NqnCX6nZP35S2FZGg+mGiNv/Lirg==",
                result
        );
    }
}