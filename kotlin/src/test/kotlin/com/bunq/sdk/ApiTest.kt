package com.bunq.sdk

import com.bunq.sdk.generated.endpoint.List_all_MonetaryAccountBank_for_User
import com.bunq.sdk.generated.endpoint.READ_User
import kotlinx.coroutines.test.runTest
import org.junit.jupiter.api.Assertions
import org.junit.jupiter.api.Test
import kotlin.test.assertEquals

private val config = Config(
    apiKey = "sandbox_83f4f88a10706750ec2fdcbc1ce97b582a986f2846d33dcaaa974d95",
    serviceName = "PeterScript"
)

class ApiTest {

    @Test
    fun test(): Unit = runTest {
        val signing = Signing(config)
        val context = initContext(config)
        val client = Client(signing, context)


        val req = READ_User.Request(
            itemId = context.userId,
            CacheControl = null,
            UserAgent = config.serviceName,
            XBunqLanguage = null,
            XBunqRegion = null,
            XBunqClientRequestId = null,
            XBunqGeolocation = null,
            XBunqClientAuthentication = config.apiKey
        )
        val res = client.rEAD_User(req)

        val body = when (res) {
            is READ_User.Response200 -> res.body
            is READ_User.Response400 -> error("Cannot read user")
        }

        assertEquals("Donald Byrne", body.UserPerson?.legal_name)
    }

    @Test
    @Throws(Exception::class)
    fun testListAllMonetaryAccountBankForUser()= runTest {
        val signing = Signing(config)
        val context = initContext(config)
        val client = Client(signing, context)

        val req = List_all_MonetaryAccountBank_for_User.Request(
            context.userId,
            null,
            config.serviceName,
            null,
            null,
            null,
            null,
            context.sessionToken,
        )

        val res: List_all_MonetaryAccountBank_for_User.Response<*> =
            client.list_all_MonetaryAccountBank_for_User(req)

        if (res is List_all_MonetaryAccountBank_for_User.Response200) {
            Assertions.assertEquals("D. Byrne", res.body[0].display_name)
        } else {
            throw RuntimeException("Cannot list monetary accounts")
        }
    }

}