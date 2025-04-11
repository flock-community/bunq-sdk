package com.bunq.sdk

import com.bunq.sdk.generated.READ_UserEndpoint
import kotlinx.coroutines.runBlocking
import org.junit.jupiter.api.Test
import kotlin.test.assertEquals

private val config = Config(
    apiKey = "sandbox_83f4f88a10706750ec2fdcbc1ce97b582a986f2846d33dcaaa974d95",
    serviceName = "PeterScript"
)

class ApiTest {

    @Test
    fun test(): Unit = runBlocking {
        val signing = Signing(config)
        val context = initContext(config)
        val client = Client(signing, context)

        val req = READ_UserEndpoint.Request(
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
            is READ_UserEndpoint.Response200 -> res.body
            is READ_UserEndpoint.Response400 -> error("Cannot read user")
        }

        assertEquals("Donald Byrne", body.UserPerson?.legal_name)

    }
}