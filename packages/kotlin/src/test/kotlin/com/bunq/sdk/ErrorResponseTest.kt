package com.bunq.sdk

import com.bunq.sdk.generated.endpoint.ReadUser
import community.flock.wirespec.kotlin.Wirespec
import org.junit.jupiter.api.Test
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith
import kotlin.test.assertIs
import kotlin.test.assertTrue

class ErrorResponseTest {

    private fun readUser(status: Int, body: String) =
        ReadUser.fromRawResponse(serialization, Wirespec.RawResponse(status, emptyMap(), body.toByteArray()))

    @Test
    fun `a 400 error body without Response envelope is deserialized`() {
        val response = readUser(400, """{"Error":[{"error_description":"Missing required field \"currency\"."}]}""")

        assertIs<ReadUser.Response400>(response)
        assertEquals("Missing required field \"currency\".", response.body.Error?.single()?.error_description)
    }

    @Test
    fun `a status other than 200 and 400 is a typed response`() {
        val response = readUser(403, """{"Error":[{"error_description":"Insufficient authentication."}]}""")

        assertIs<ReadUser.Response403>(response)
        assertEquals("Insufficient authentication.", response.body.Error?.single()?.error_description)
    }

    @Test
    fun `a body without Response or Error is rejected`() {
        assertFailsWith<IllegalStateException> { readUser(200, """{"unexpected":true}""") }
    }

    @Test
    fun `a non-JSON error body names the status`() {
        val html = Wirespec.RawResponse(500, emptyMap(), "<html>Internal Server Error</html>".toByteArray())

        val e = assertFailsWith<IllegalStateException> { html.failOnNonJsonError() }

        assertTrue("500" in e.message!! && "<html>" in e.message!!)
    }
}
