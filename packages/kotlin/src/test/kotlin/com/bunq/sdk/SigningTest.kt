package com.bunq.sdk

import org.junit.jupiter.api.Test
import java.io.File
import kotlin.test.assertEquals


class SigningTest {

    @Test
    fun signing() {
        val config = Config(
            serviceName = "",
            apiKey = "",
            publicKeyFile = File("../../public_key.pem"),
            privateKeyFile = File("../../private_key.pem"),

        )
        val signing = Signing(config)
        val res = signing.signData("Hello")
        assertEquals(
            "T/jCqiFSe1nj9keIq2Cdg5MISs69IIJa1BcmsQ+0iLTuKWNrbOcSS7lvEF7HSWiW8i7Vu4ofhTaw+iob75UB9qVpy8gZBd6UMSWKNUMDXtqj0LbUcov191m6eYLEme9hkg4R/5L9eEaTGvMuuEjxJ05/GgJe2wj2hhun1WoKGBaNCV9y7UrT6CXODMl45AprtttCpB5smjaCtfnW6NaIijHRanKjjIKLu7XaxYVuEFEYvsgm+aQKdKa1gi90qT48zt/R8MNLqoOH1P4NHAXXnplTh5j1BJEDKk1QMsZBS71KhbQU3y3dRjjf/+NqnCX6nZP35S2FZGg+mGiNv/Lirg==",
            res
        )
    }
}