import kotlinx.serialization.json.Json
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive
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

    @Test
    fun `every operation answers the bunq error statuses like its 400`() {
        val error = """{"${'$'}ref":"#/components/responses/GenericError"}"""
        val spec = """{"openapi":"3.0.0","paths":{"/a":{"get":{"operationId":"READ_A","responses":{"200":{"description":"ok"},"400":$error,"404":{"description":"own"}}}}}}"""
        val responses = Json.parseToJsonElement(OpenApiPreProcessor(spec)).jsonObject["paths"]!!.jsonObject["/a"]!!
            .jsonObject["get"]!!.jsonObject["responses"]!!.jsonObject
        assertEquals(setOf("200", "400", "401", "403", "404", "405", "429", "466", "490", "491", "500"), responses.keys)
        assertEquals(Json.parseToJsonElement(error), responses["403"])
        assertEquals("own", responses["404"]!!.jsonObject["description"]!!.jsonPrimitive.content)
    }

    @Test
    fun `the inline generic error body becomes a shared named schema`() {
        val inline = """{"type":"object","properties":{"Error":{"type":"array"}}}"""
        val spec = """{"openapi":"3.0.0","components":{"schemas":{},"responses":{"GenericError":{"content":{"application/json":{"schema":$inline}}}}}}"""
        val components = Json.parseToJsonElement(OpenApiPreProcessor(spec)).jsonObject["components"]!!.jsonObject
        assertEquals(Json.parseToJsonElement(inline), components["schemas"]!!.jsonObject["GenericError"])
        assertEquals(
            Json.parseToJsonElement("""{"${'$'}ref":"#/components/schemas/GenericError"}"""),
            components["responses"]!!.jsonObject["GenericError"]!!.jsonObject["content"]!!.jsonObject["application/json"]!!.jsonObject["schema"]
        )
    }

    @Test
    fun `an operation without a 400 response gets no extra statuses`() {
        val spec = """{"openapi":"3.0.0","paths":{"/a":{"get":{"operationId":"READ_A","responses":{"200":{"description":"ok"}}}}}}"""
        val responses = Json.parseToJsonElement(OpenApiPreProcessor(spec)).jsonObject["paths"]!!.jsonObject["/a"]!!
            .jsonObject["get"]!!.jsonObject["responses"]!!.jsonObject
        assertEquals(setOf("200"), responses.keys)
    }

    @Test
    fun `an existing GenericError schema is not overwritten`() {
        val inline = """{"type":"object"}"""
        val spec = """{"openapi":"3.0.0","components":{"schemas":{"GenericError":{}},"responses":{"GenericError":{"content":{"application/json":{"schema":$inline}}}}}}"""
        assertFailsWith<IllegalStateException> { OpenApiPreProcessor(spec) }
    }
}
