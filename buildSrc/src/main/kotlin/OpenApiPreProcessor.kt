import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonArray
import kotlinx.serialization.json.JsonElement
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.JsonPrimitive
import kotlinx.serialization.json.buildJsonObject
import kotlinx.serialization.json.contentOrNull
import kotlinx.serialization.json.jsonArray
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive
import kotlinx.serialization.json.put
import java.io.Serializable

/**
 * Pre-processor for OpenAPI schemas that filters out specific parameters.
 * This processor is used in the Wirespec task to modify the OpenAPI schema before code generation.
 *
 * It edits the raw JSON tree so it does not depend on the OpenAPI model of the Wirespec compiler, which changes between versions.
 */
object OpenApiPreProcessor : (String) -> String, Serializable {
    /**
     * List of parameter names that should be filtered out from the OpenAPI schema.
     */
    private val filterParams = listOf(
        "Cache-Control",
        "User-Agent",
        "X-Bunq-Language",
        "X-Bunq-Region",
        "X-Bunq-Client-Request-Id",
        "X-Bunq-Geolocation",
        "X-Bunq-Client-Authentication"
    )

    private val wrapResponse = mapOf(
        "DeviceServerCreate" to "Id",
        "MonetaryAccountBankRead" to "MonetaryAccountBank",
        "SandboxUserPersonCreate" to "ApiKey"
    )

    private val createInputSchemas = mapOf(
        "RequestInquiry" to "CreateRequestInquiry"
    )

    private val updateRequestBodyType = mapOf(
        "CREATE_RequestInquiry_for_User_MonetaryAccount" to "CreateRequestInquiry"
    )

    private val operationKeys = listOf("get", "post", "put", "delete", "patch", "options", "head")

    private fun schemaRef(name: String) = buildJsonObject { put("\$ref", "#/components/schemas/$name") }

    private fun JsonElement.isRef() = this is JsonObject && "\$ref" in this

    // OpenAPI 3.0 ignores siblings of $ref; the Wirespec parser rejects them.
    private fun JsonElement.withoutRefSiblings(): JsonElement = when (this) {
        is JsonObject -> this["\$ref"]?.let { JsonObject(mapOf("\$ref" to it)) }
            ?: JsonObject(mapValues { (_, value) -> value.withoutRefSiblings() })
        is JsonArray -> JsonArray(map { it.withoutRefSiblings() })
        else -> this
    }

    /**
     * Filters a parameter to determine if it should be included in the processed schema.
     */
    private fun shouldKeepParameter(parameter: JsonElement): Boolean {
        val obj = parameter.jsonObject
        val ref = obj["\$ref"]?.jsonPrimitive?.contentOrNull
        return if (ref != null) {
            ref !in filterParams.map { "#/components/parameters/$it" }
        } else {
            obj["name"]?.jsonPrimitive?.contentOrNull !in filterParams
        }
    }

    private fun queryParameter(name: String, description: String, schema: JsonObject) = buildJsonObject {
        put("name", name)
        put("in", "query")
        put("required", false)
        put("description", description)
        put("schema", schema)
    }

    private fun integerSchema(maximum: Double? = null) = buildJsonObject {
        put("type", "integer")
        maximum?.let { put("maximum", it) }
    }

    /**
     * Pagination is not listed in the original openapi spec, but is allowed on every 'List' endpoint
     *
     * https://doc.bunq.com/#/pagination
     *
     */
    private val paginationParams = listOf(
        queryParameter(
            "count",
            "Pagination parameter. The count value can be indicate the number of items requested. The items in the response always less than or equal to the maximum count value specified in the request.",
            integerSchema(maximum = 200.0)
        ),
        queryParameter(
            "newer_id",
            "Pagination parameter. Returns the items newer than this id. Items are listed newest first, so to get the page before the current one pass the id of its first item (the newer_id in newer_url). If newer_url is null, there are no newer items.",
            integerSchema()
        ),
        queryParameter(
            "older_id",
            "Pagination parameter. Returns the items older than this id. Items are listed newest first, so to get the page after the current one pass the id of its last item (the older_id in older_url). If older_url is null, there are no older items.",
            integerSchema()
        )
    )

    /** bunq returns `{"Response": [...], "Pagination": {...}}` for lists; the spec only documents the array. */
    private val paginationSchema = buildJsonObject {
        put("type", "object")
        put("properties", buildJsonObject {
            listOf("future_url", "newer_url", "older_url").forEach { name ->
                put(name, buildJsonObject {
                    put("type", "string")
                    put("nullable", true)
                })
            }
        })
    }

    /** `MonetaryAccountBankListing` -> `MonetaryAccountBankPage`. */
    private fun pageSchemaName(itemSchemaName: String) = itemSchemaName.removeSuffix("Listing") + "Page"

    private fun pageSchema(itemRef: JsonElement) = buildJsonObject {
        put("type", "object")
        put("properties", buildJsonObject {
            put("Response", buildJsonObject {
                put("type", "array")
                put("items", itemRef)
            })
            put("Pagination", schemaRef("Pagination"))
        })
        put("required", JsonArray(listOf("Response", "Pagination").map(::JsonPrimitive)))
    }

    /**
     * Replaces the array schema of a list operation's 200 response by a named page schema and records it in [pages].
     * The responses that do not have an array of schema references are left as they are.
     */
    private fun withPagedResponse(responses: JsonElement, pages: MutableMap<String, JsonElement>): JsonElement {
        val ok = (responses as? JsonObject)?.get("200") as? JsonObject ?: return responses
        val content = ok["content"] as? JsonObject ?: return responses
        val paged = content.mapValues { (_, mediaType) ->
            val schema = (mediaType as? JsonObject)?.get("schema") as? JsonObject
            val items = schema?.get("items")
            val itemName = (items as? JsonObject)?.get("\$ref")?.jsonPrimitive?.contentOrNull?.substringAfterLast('/')
            if (schema?.get("type")?.jsonPrimitive?.contentOrNull != "array" || items == null || itemName == null) {
                mediaType
            } else {
                val name = pageSchemaName(itemName)
                pages[name] = pageSchema(items)
                JsonObject(mediaType.jsonObject + ("schema" to schemaRef(name)))
            }
        }
        return JsonObject(responses + ("200" to JsonObject(ok + ("content" to JsonObject(paged)))))
    }

    private val createRequestInquirySchema = buildJsonObject {
        put("type", "object")
        put("properties", buildJsonObject {
            put("amount_inquired", schemaRef("Amount"))
            put("counterparty_alias", schemaRef("Pointer"))
            put("description", buildJsonObject {
                put("type", "string")
                put("description", "The description for the RequestInquiry")
            })
            put("allow_bunqme", buildJsonObject {
                put("type", "boolean")
                put("description", "Whether or not sending a bunq.me request is allowed")
            })
        })
        put("required", JsonArray(
            listOf("amount_inquired", "counterparty_alias", "description", "allow_bunqme").map(::JsonPrimitive)
        ))
    }

    private fun processSchemas(schemas: JsonObject): JsonObject {
        val processed = schemas.mapValues { (key, schema) ->
            wrapResponse[key]?.takeUnless { schema.isRef() }?.let { prop ->
                buildJsonObject {
                    put("type", "object")
                    put("properties", buildJsonObject { put(prop, schema) })
                }
            } ?: schema
        }.toMutableMap()
        createInputSchemas.forEach { (originalKey, inputKey) ->
            if (schemas[originalKey]?.isRef() == false) processed[inputKey] = createRequestInquirySchema
        }
        return JsonObject(processed)
    }

    /** `READ_User` -> `readUser`, `List_all_User_for_Thing` -> `listAllUserForThing`. */
    internal fun camelCaseOperationId(operationId: String): String =
        operationId.split("_").filter { it.isNotEmpty() }.mapIndexed { index, word ->
            val normalised = if (word.all { !it.isLetter() || it.isUpperCase() }) word.lowercase() else word
            if (index == 0) normalised.replaceFirstChar { it.lowercase() } else normalised.replaceFirstChar { it.uppercase() }
        }.joinToString("")

    private fun processOperation(operation: JsonObject, pages: MutableMap<String, JsonElement>): JsonObject {
        val operationId = operation["operationId"]?.jsonPrimitive?.contentOrNull
        val result = operation.toMutableMap()

        operation["parameters"]?.let { parameters ->
            val kept = parameters.jsonArray.filter(::shouldKeepParameter)
            val withPagination = if (operationId?.startsWith("List_") == true) kept + paginationParams else kept
            result["parameters"] = JsonArray(withPagination)
        }

        if (operationId?.startsWith("List_") == true) {
            operation["responses"]?.let { result["responses"] = withPagedResponse(it, pages) }
        }

        updateRequestBodyType[operationId]?.let { newReference ->
            val requestBody = operation["requestBody"]
            println("Updating request body for $operationId: $requestBody")
            if (requestBody is JsonObject && !requestBody.isRef()) {
                result["requestBody"] = JsonObject(requestBody.toMutableMap().also { body ->
                    body["content"]?.jsonObject?.let { content ->
                        body["content"] = JsonObject(content.mapValues { (_, mediaType) ->
                            JsonObject(mediaType.jsonObject + ("schema" to schemaRef(newReference)))
                        })
                    }
                })
            }
        }
        operationId?.let { result["operationId"] = JsonPrimitive(camelCaseOperationId(it)) }
        return JsonObject(result)
    }

    private fun requireUniqueOperationIds(paths: JsonObject) {
        val collisions = paths.values.flatMap { item ->
            item.jsonObject.filterKeys { it in operationKeys }.values.mapNotNull {
                it.jsonObject["operationId"]?.jsonPrimitive?.contentOrNull
            }
        }.groupBy { it }.filterValues { it.size > 1 }.keys
        check(collisions.isEmpty()) { "Operation ids collide after camelCase rewrite: $collisions" }
    }

    private fun processPathItem(pathItem: JsonObject, pages: MutableMap<String, JsonElement>): JsonObject =
        JsonObject(pathItem.mapValues { (key, value) ->
            if (key in operationKeys && value is JsonObject) processOperation(value, pages) else value
        })

    /**
     * Processes an OpenAPI schema by filtering out specified parameters.
     *
     * @param schema The OpenAPI schema as a JSON string.
     * @return The processed OpenAPI schema as a JSON string.
     */
    override fun invoke(schema: String): String {
        val openApi = Json.parseToJsonElement(schema).withoutRefSiblings().jsonObject
        val processed = openApi.toMutableMap()

        val pages = mutableMapOf<String, JsonElement>()
        openApi["paths"]?.jsonObject?.let { paths ->
            val processedPaths = JsonObject(paths.mapValues { (_, item) -> processPathItem(item.jsonObject, pages) })
            requireUniqueOperationIds(processedPaths)
            processed["paths"] = processedPaths
        }
        openApi["components"]?.jsonObject?.let { components ->
            processed["components"] = JsonObject(components.toMutableMap().also { result ->
                components["schemas"]?.jsonObject?.let { schemas ->
                    val added = if (pages.isEmpty()) emptyMap() else pages + ("Pagination" to paginationSchema)
                    val collisions = added.keys.filter { it in schemas }
                    check(collisions.isEmpty()) { "Schemas to add already exist: $collisions" }
                    result["schemas"] = JsonObject(processSchemas(schemas) + added)
                }
            })
        }
        return Json.encodeToString(JsonObject.serializer(), JsonObject(processed))
    }
}
