package com.bunq.sdk

import com.bunq.sdk.generated.Sdk
import com.bunq.sdk.generated.endpoint.CREATE_RequestInquiry_for_User_MonetaryAccount
import com.bunq.sdk.generated.endpoint.List_all_MonetaryAccountBank_for_User
import com.bunq.sdk.generated.endpoint.READ_MonetaryAccountBank_for_User
import com.bunq.sdk.generated.endpoint.READ_User
import com.bunq.sdk.generated.model.Amount
import com.bunq.sdk.generated.model.CreateRequestInquiry
import com.bunq.sdk.generated.model.MonetaryAccountBankRead
import com.bunq.sdk.generated.model.Pointer
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay
import kotlinx.coroutines.test.runTest
import kotlinx.coroutines.withContext
import org.junit.jupiter.api.Assertions
import org.junit.jupiter.api.Disabled
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.fail
import java.math.BigDecimal
import kotlin.collections.firstOrNull
import kotlin.test.assertEquals
import kotlin.test.assertNotNull
import kotlin.test.assertTrue
import kotlin.time.Duration.Companion.seconds


private val config = Config(
    bunqServer = BUNQ_SANDBOX_SERVER,
    apiKey = "sandbox_83f4f88a10706750ec2fdcbc1ce97b582a986f2846d33dcaaa974d95",
    serviceName = "PeterScript",
    signingKeys = SigningKeys.FromPem(
        """
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
        """
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
    )
)

class ApiTest {

    @Test
    fun `testREADUser`(): Unit = runTest {
        val context = initContext(config)
        val handler = handler(context)
        val sdk = Sdk(handler)

        val res = sdk.rEAD_User(context.userId)
        val body = when (res) {
            is READ_User.Response200 -> res.body
            is READ_User.Response400 -> error("Cannot read user")
        }
        assertEquals("Donald Byrne", body.UserPerson?.legal_name)
    }

    @Test
    fun `testbankAccount`(): Unit = runTest {
        val context = initContext(config)
        val sdk = Sdk(handler(context))
        val res = sdk.list_all_MonetaryAccountBank_for_User(context.userId, null, null, null)
        val body = when (res) {
            is List_all_MonetaryAccountBank_for_User.Response200 -> res.body
            is List_all_MonetaryAccountBank_for_User.Response400 -> error("Could not get bank accounts")
        }
        assertEquals(1989601, body.firstOrNull()?.id)
        assertEquals("EUR", body.firstOrNull()?.balance?.currency)
        assertTrue { (body.firstOrNull()?.balance?.value?.toBigDecimal() ?: BigDecimal.ZERO) > BigDecimal.ZERO }
    }

    @Test
    fun `testbankAccount1`(): Unit = runTest {
        val context = initContext(config)
        val sdk = Sdk(handler(context))
        val body = getBankAccount(sdk, context)
        assertEquals(1989601, body.MonetaryAccountBank?.id)
        assertTrue { (body.MonetaryAccountBank?.balance?.value?.toBigDecimal() ?: BigDecimal.ZERO) > BigDecimal.ZERO }
    }

    private suspend fun getBankAccount(
        sdk: Sdk,
        context: Context
    ): MonetaryAccountBankRead {
        val res = sdk.rEAD_MonetaryAccountBank_for_User(context.userId, 1989601)
        val body = when (res) {
            is READ_MonetaryAccountBank_for_User.Response200 -> res.body
            is READ_MonetaryAccountBank_for_User.Response400 -> fail("Could not get bank account")
        }
        return body
    }

    @Test
    @Throws(Exception::class)
    fun testListAllMonetaryAccountBankForUser() = runTest {
        val context = initContext(config)
        val sdk = Sdk(handler(context))
        val res: List_all_MonetaryAccountBank_for_User.Response<*> =
            sdk.list_all_MonetaryAccountBank_for_User(
                userID = context.userId,
                count = null,
                newer_id = null,
                older_id = null
            )
        if (res is List_all_MonetaryAccountBank_for_User.Response200) {
            assertEquals("D. Byrne", res.body[0].display_name)
        } else {
            fail { "Cannot list monetary accounts" }
        }
    }

    @Test
    fun `refresh a session`() = runTest {
        val context = initContext(config)
        val sdk = Sdk(handler(context))

        val res = sdk.list_all_MonetaryAccountBank_for_User(
            userID = context.userId,
            count = null,
            newer_id = null,
            older_id = null
        )
        val body = when (res) {
            is List_all_MonetaryAccountBank_for_User.Response200 -> res.body
            is List_all_MonetaryAccountBank_for_User.Response400 -> fail("Could not get bank accounts")
        }
        assertEquals(1, body.size)
        val monetaryAccountBankListing = body.firstOrNull()
        assertNotNull(monetaryAccountBankListing)
        assertEquals(1989601, monetaryAccountBankListing.id)
        assertTrue { (body.firstOrNull()?.balance?.value?.toBigDecimal() ?: BigDecimal.ZERO) > BigDecimal.ZERO }

        val refreshSession = context.refreshSession()
        val refreshedSdk = Sdk(handler(refreshSession))

        val res2 = refreshedSdk.list_all_MonetaryAccountBank_for_User(
            userID = context.userId,
            count = null,
            newer_id = null,
            older_id = null
        )
        val body2 = when (res2) {
            is List_all_MonetaryAccountBank_for_User.Response200 -> res2.body
            is List_all_MonetaryAccountBank_for_User.Response400 -> fail("Could not get bank accounts")
        }
        val monetaryAccountBankListing2 = body2.firstOrNull()
        assertNotNull(monetaryAccountBankListing2)
        assertEquals(monetaryAccountBankListing2, monetaryAccountBankListing)


    }

    @Disabled("Slow test, deliberately there to validate create request inquiry works")
    @Test
    fun `request spending money`() = runTest {
        val context = initContext(config)
        val sdk = Sdk(handler(context))

        val bankAccount = getBankAccount(sdk, context)
        println("Bank account: ${bankAccount.MonetaryAccountBank?.balance?.value}")
        val response = sdk.cREATE_RequestInquiry_for_User_MonetaryAccount(
            context.userId,
            bankAccount.MonetaryAccountBank?.id!!,
            CreateRequestInquiry(
                amount_inquired = Amount("0.01", "EUR"),
                counterparty_alias = Pointer(
                    "EMAIL", "sugardaddy@bunq.com", "Suggar Daddy", null
                ),
                description = "Just testing. Have some cents?",
                allow_bunqme = false,
            )
        )


        when (response) {
            is CREATE_RequestInquiry_for_User_MonetaryAccount.Response200 -> {
                println("Received requestInquiry okay. Waiting for 10 seconds to ensure balance is updated")
                withContext(Dispatchers.Default) {
                    repeat(10) {
                        delay(1.seconds) // Dispatchers.Default doesn't know about TestCoroutineScheduler
                        println("${it + 1}" + " . ".repeat(it + 1))
                    }
                    println()
                }
                println("Fetching bank account again")
                val bankAccount1 = getBankAccount(sdk, context)
                println("Bank account after request inquiry: ${bankAccount1.MonetaryAccountBank?.balance?.value}")

                assertTrue {
                    (bankAccount1.MonetaryAccountBank?.balance?.value?.toBigDecimal()
                        ?: BigDecimal.ZERO) > (bankAccount.MonetaryAccountBank.balance?.value?.toBigDecimal()
                        ?: BigDecimal.ONE)
                }
            }

            is CREATE_RequestInquiry_for_User_MonetaryAccount.Response400 -> fail("ahh, failure")
        }
    }
}