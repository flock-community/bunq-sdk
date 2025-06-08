package com.bunq.sdk

import com.bunq.sdk.generated.Sdk
import com.bunq.sdk.generated.endpoint.List_all_MonetaryAccountBank_for_User
import com.bunq.sdk.generated.endpoint.READ_User
import kotlinx.coroutines.test.runTest
import org.junit.jupiter.api.Assertions
import org.junit.jupiter.api.Test
import java.io.File
import kotlin.test.assertEquals

private val config = Config(
    apiKey = "sandbox_83f4f88a10706750ec2fdcbc1ce97b582a986f2846d33dcaaa974d95",
    serviceName = "PeterScript",
    publicKeyFile = File("../../public_key.pem"),
    privateKeyFile = File("../../private_key.pem"),
)

class ApiTest {

    @Test
    fun `testREADUser`(): Unit = runTest {
        val signing = Signing(config)
        val context = initContext(config)
        val sdk = Sdk(handler(signing, context))
        val res = sdk.rEAD_User(context.userId,)
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
        val sdk = Sdk(handler(signing, context))
        val res: List_all_MonetaryAccountBank_for_User.Response<*> =
            sdk.list_all_MonetaryAccountBank_for_User(context.userId)
        if (res is List_all_MonetaryAccountBank_for_User.Response200) {
            Assertions.assertEquals("D. Byrne", res.body[0].display_name)
        } else {
            throw RuntimeException("Cannot list monetary accounts")
        }
    }
}