import kotlinx.serialization.json.Json
import kotlinx.serialization.json.jsonArray
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive
import kotlin.test.Test
import kotlin.test.assertContains
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

    @Test
    fun `pagination parameters describe the sandbox behaviour`() {
        val spec = """{"openapi":"3.0.0","paths":{"/a":{"get":{"operationId":"List_all_User","parameters":[]}}}}"""
        val params = Json.parseToJsonElement(OpenApiPreProcessor(spec)).jsonObject["paths"]!!.jsonObject["/a"]!!
            .jsonObject["get"]!!.jsonObject["parameters"]!!.jsonArray.associate {
                it.jsonObject["name"]!!.jsonPrimitive.content to it.jsonObject["description"]!!.jsonPrimitive.content
            }
        assertEquals(listOf("count", "newer_id", "older_id"), params.keys.toList())
        assertContains(params.getValue("newer_id"), "newer than this id")
        assertContains(params.getValue("newer_id"), "first item")
        assertContains(params.getValue("older_id"), "older than this id")
        assertContains(params.getValue("older_id"), "last item")
    }
}
