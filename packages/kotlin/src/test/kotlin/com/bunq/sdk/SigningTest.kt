package com.bunq.sdk

import org.junit.jupiter.api.Test
import kotlin.test.assertEquals


class SigningTest {

    @Test
    fun signing() {

        val config = Config(
            bunqServer = BUNQ_SANDBOX_SERVER,
            serviceName = "test",
            apiKey = "test",
            signingKeys = SigningKeys.FromPem(


                publicKeyAsPem = """
                |-----BEGIN PUBLIC KEY-----
                |MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnNN/tvunpRQby6Nv5Jpd
                |CcpQd7Jh135NByStNoS9BcTGOiURVp06q1MjCO84uCr7gNOg7F4WnB9GWZBjeEmq
                |ydDcBYvDSuNGaZMk2IM7PNDqoczjZyraXxGbYBCjpxKHRcdsZ6dA8y1VrRb56Q3D
                |/HUOuZJZhurQ5p592cjy0MuGDib3pkmlNxNYtQI9G/o128o/12C73PNxPP+BZUdf
                |N7oGg0aUzfzcFO2eUo//K8iOCX92mIlTiD/ptGmCc7zyfAAgtm3uFzWwSks5nXjx
                |UWmmCQB0dhg2j2teZOcUJDM8h/QoNnl6TtZZzmOb5WFGQQjLWEMaVH3+SHWUYeFU
                |rQIDAQAB
                |-----END PUBLIC KEY-----
            """.trimMargin(),
                privateKeyAsPem = """
                |-----BEGIN PRIVATE KEY-----
                |MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCc03+2+6elFBvL
                |o2/kml0JylB3smHXfk0HJK02hL0FxMY6JRFWnTqrUyMI7zi4KvuA06DsXhacH0ZZ
                |kGN4SarJ0NwFi8NK40ZpkyTYgzs80OqhzONnKtpfEZtgEKOnEodFx2xnp0DzLVWt
                |FvnpDcP8dQ65klmG6tDmnn3ZyPLQy4YOJvemSaU3E1i1Aj0b+jXbyj/XYLvc83E8
                |/4FlR183ugaDRpTN/NwU7Z5Sj/8ryI4Jf3aYiVOIP+m0aYJzvPJ8ACC2be4XNbBK
                |SzmdePFRaaYJAHR2GDaPa15k5xQkMzyH9Cg2eXpO1lnOY5vlYUZBCMtYQxpUff5I
                |dZRh4VStAgMBAAECggEAGL9IRVIHZaWbcEJJbyfLvDaEharsxSJdWd34BmUiZeVk
                |CXtddc9IWY48NlX3m5pOx0i9+WashzTpN0txYuMvE/tFKQvhxLDCJPlPBGqK/8EQ
                |8XjhPp+0x3FCFUHy7TOfjIuYZ+/s8CLMhQyd4aCmN3GqYe69+WwXDHlgrywGYxun
                |SPdyk2WYhYp/3yLdN8fELM2kJPuHI5Bu25dkSc/fhaUVDgdKX84/SByhKfzq0zya
                |3WbrPGhyoQytey5GLxi0Q4UGHBkNEMYDdVMYorEnzfZOksy3Dp+n4xvu6793cLBU
                |C987jknCSb3IFjys3MTPwNdA1+f8SfmhQOcSPTclIQKBgQDZUBYBKmzAh2v8uh94
                |EtnTJS1LAItwgWrqCwwsbOrydhU9KHCIpzHZVbsFcHOjOFPZVYi6XnVQbacJAGDx
                |CqWH6+h8WMMJVxybsVAPsjKkRfbT/KZrgcYFDP4qISMEXp6v+BrMbi/XIEiB4tWT
                |1YJiqm7TdgIDeV7A1NtNoIf2oQKBgQC4vsQYJaDBYi3mTVxEHPLdMc5cTUIlr5JL
                |phDEdqVatD/KlWbcZ6IYqfLRW03zy2r/8VQGCp7B7ssj2iE585fRohNB5C7j8BaA
                |E9DBQHoa4+BeW461e0mCuiI/irhK58Pfeg1rBJlnyNgfRe51Vw2Bqev64zFlhnWF
                |T8zewBO+jQKBgQCCqLBSSxvQNpwq/A1nuI3XcgbljZJJNsb9qV7MZ0BsP6tNdj8T
                |KtPCBNXJ027zuC5SAiePRrPqg8Nmmh+vTeNw8dp6yTObLhE5W0bz6QSh2J8rnkDB
                |aumQp9s5oWrYebuXuekC+U0yX2q5DZW0qS8X+7le0xkq1ZKvBkxFRDv7gQKBgBGZ
                |Qo7WTsj9NEgjCG4In+4IR5MtXObAIdyI9kHw13GbiBQhRUorqRpWXiYpX3Sg5RF6
                |iLmGm3b362v/5HhjxwuWN+Vn+juGbG5I9PLj1H3pRT9X03FgTDFiz85jxYiFKXiJ
                |ZOvT5VUoocXg4IVXBJdce3lL2THFrD5FystRWtAlAoGABTdVLZ4iHuEHClRMgxXM
                |+kJ1iRyz54nDySJI7922TYt9LmMOWhWqijAuLbbbZ7PAsxtO6TCqUdSsy+Jx2Y2G
                |PO/olJBKnIN3f0MpCBz5oFBMkfNsbQ4bPVD2V3pwcdf2HLydTwk49o6WZFar/FGG
                |os8c7u7MfsR3Tl/MGtJGsH0=
                |-----END PRIVATE KEY-----
                """.trimMargin(),
                )
        )
        val res = Signing.signData(config, "Hello")
        assertEquals(
            "fR0Gyn8VfC8eCwq10x5eYAcxXh4nv6331hWAAr77l72zfFScbw3hFSE6iBNklCYc0mfnKezsuRo3re+fTNNHO1oZhfhjc9i4UYxTxBiOEslHrKx9NkXkBZh2RALx/LnhlpyMwB5BBOlFlNeR9Hyj5E8c/a2pObBZRmrZ3cgAnoWF8hhY5Y9XwLS2WIodYIPSQXuQMXyi1UBxhxAbniZ5m1uRSt8gaPmQGMCQtUzvZ8KUXtSvugGPsXHwh94EccZCfjS0sdIQK8AcZ8t5YL6bqkqJ7eVzbxoX6U1nOZVy3MxQMKQ/PFS297er6qsVsGwKbNfaTUvymEb46mM/gQdQDQ==",
            res
        )
    }
}