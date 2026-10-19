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

    @Test
    fun `list responses become a named page with items and pagination`() {
        val spec = """
            {"openapi":"3.0.0",
             "paths":{
               "/a":{"get":{"operationId":"List_all_Thing","responses":{"200":{"description":"ok","content":{"application/json":{"schema":{"type":"array","items":{"${'$'}ref":"#/components/schemas/ThingListing"}}}}}}}},
               "/b":{"get":{"operationId":"READ_Thing","responses":{"200":{"description":"ok","content":{"application/json":{"schema":{"${'$'}ref":"#/components/schemas/ThingRead"}}}}}}}},
             "components":{"schemas":{"ThingListing":{"type":"object"},"ThingRead":{"type":"object"}}}}
        """
        val out = Json.parseToJsonElement(OpenApiPreProcessor(spec)).jsonObject
        fun responseSchema(path: String) = out["paths"]!!.jsonObject[path]!!.jsonObject["get"]!!.jsonObject["responses"]!!
            .jsonObject["200"]!!.jsonObject["content"]!!.jsonObject["application/json"]!!.jsonObject["schema"]!!.jsonObject
        val schemas = out["components"]!!.jsonObject["schemas"]!!.jsonObject

        assertEquals("#/components/schemas/ThingPage", responseSchema("/a")["${'$'}ref"]!!.jsonPrimitive.content)
        assertEquals("#/components/schemas/ThingRead", responseSchema("/b")["${'$'}ref"]!!.jsonPrimitive.content)
        val page = schemas["ThingPage"]!!.jsonObject
        assertEquals(listOf("Response", "Pagination"), page["properties"]!!.jsonObject.keys.toList())
        assertEquals(
            "#/components/schemas/ThingListing",
            page["properties"]!!.jsonObject["Response"]!!.jsonObject["items"]!!.jsonObject["${'$'}ref"]!!.jsonPrimitive.content
        )
        assertEquals(
            listOf("future_url", "newer_url", "older_url"),
            schemas["Pagination"]!!.jsonObject["properties"]!!.jsonObject.keys.toList()
        )
    }
}
