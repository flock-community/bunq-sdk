import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith

class OpenApiPreProcessorTest {

    @Test
    fun `operation ids become camelCase`() {
        assertEquals("readUser", OpenApiPreProcessor.camelCaseOperationId("READ_User"))
        assertEquals("listAllUserForThing", OpenApiPreProcessor.camelCaseOperationId("List_all_User_for_Thing"))
        assertEquals(
            "createRequestInquiryForUserMonetaryAccount",
            OpenApiPreProcessor.camelCaseOperationId("CREATE_RequestInquiry_for_User_MonetaryAccount")
        )
    }

    @Test
    fun `digits, acronyms and mixed case segments`() {
        assertEquals("readGeneratedCvc2ForUserCard", OpenApiPreProcessor.camelCaseOperationId("READ_GeneratedCvc2_for_User_Card"))
        assertEquals("readIbanForUser", OpenApiPreProcessor.camelCaseOperationId("READ_IBAN_for_User"))
        assertEquals("readOAuthClientForUser", OpenApiPreProcessor.camelCaseOperationId("READ_OAuthClient_for_User"))
    }

    @Test
    fun `colliding operation ids fail the build`() {
        val op = { id: String -> """{"operationId":"$id"}""" }
        val spec = """{"openapi":"3.0.0","paths":{"/a":{"get":${op("READ_User")}},"/b":{"get":${op("Read_User")}}}}"""
        assertFailsWith<IllegalStateException> { OpenApiPreProcessor(spec) }
    }
}
