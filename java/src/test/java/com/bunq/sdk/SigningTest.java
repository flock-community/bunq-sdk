package com.bunq.sdk;

import org.junit.jupiter.api.Test;

import java.io.File;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class SigningTest {

    @Test
    public void testSigning() {
        File privateKeyFile = new File("../private_key.pem");
        File publicKeyFile = new File("../public_key.pem");

        Config config = new Config(
                "",
                "",
                privateKeyFile,
                publicKeyFile
        );

        Signing signing = new Signing(config);
        String result = signing.signData("Hello");

        assertEquals(
                "DGc2wKIt8pgv/SM6XFuRheQ/UxLa3B0C7bNtiuXnkXQjA6INYTOcuNW77xRJgm2dsU2+12JHQIaN2ABTIL2R9U1k3M+z+AWDu5xGfSSjifDGBvfEhwl7QVkuyWR6IAHtmiE8j8cI6lR4d89yovIx+qio9QAOpIQ7nAHeozOzY2uLqfivDJzlSjaH3UK/UgMPkQ7+yVBariqycT+dj8RHDft2TTz6L3um9+lYqJq0IcwsHoItn7SEahLC3pYQHN9WjZUL5tsaFi2UjWEqPxBSG8fUEmKrXfS0ZZorJbNvRE9Ou/vZYOA4Vwa0nsjeMjpPTgRTLZmNDfzqa3K3Cj8ogA==",
                result
        );
    }
}