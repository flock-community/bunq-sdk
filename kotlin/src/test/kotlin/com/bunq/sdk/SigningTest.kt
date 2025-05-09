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
            publicKeyFile = File("../public_key.pem"),
            privateKeyFile = File("../private_key.pem"),

        )
        val signing = Signing(config)
        val res = signing.signData("Hello")
        assertEquals(
            "DGc2wKIt8pgv/SM6XFuRheQ/UxLa3B0C7bNtiuXnkXQjA6INYTOcuNW77xRJgm2dsU2+12JHQIaN2ABTIL2R9U1k3M+z+AWDu5xGfSSjifDGBvfEhwl7QVkuyWR6IAHtmiE8j8cI6lR4d89yovIx+qio9QAOpIQ7nAHeozOzY2uLqfivDJzlSjaH3UK/UgMPkQ7+yVBariqycT+dj8RHDft2TTz6L3um9+lYqJq0IcwsHoItn7SEahLC3pYQHN9WjZUL5tsaFi2UjWEqPxBSG8fUEmKrXfS0ZZorJbNvRE9Ou/vZYOA4Vwa0nsjeMjpPTgRTLZmNDfzqa3K3Cj8ogA==",
            res
        )
    }
}