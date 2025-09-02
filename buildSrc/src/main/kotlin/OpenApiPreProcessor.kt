import community.flock.kotlinx.openapi.bindings.v3.OpenAPI
import community.flock.kotlinx.openapi.bindings.v3.OperationObject
import community.flock.kotlinx.openapi.bindings.v3.ParameterLocation
import community.flock.kotlinx.openapi.bindings.v3.ParameterObject
import community.flock.kotlinx.openapi.bindings.v3.PathItemObject
import community.flock.kotlinx.openapi.bindings.v3.Ref
import community.flock.kotlinx.openapi.bindings.v3.ReferenceObject
import community.flock.kotlinx.openapi.bindings.v3.RequestBodyObject
import community.flock.kotlinx.openapi.bindings.v3.SchemaObject
import community.flock.kotlinx.openapi.bindings.v3.Type
import kotlinx.serialization.json.Json
import java.io.Serializable

/**
 * Pre-processor for OpenAPI schemas that filters out specific parameters.
 * This processor is used in the Wirespec task to modify the OpenAPI schema before code generation.
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

    /**
     * Extension function to apply a transformation to all operation objects in a path item.
     *
     * @param block The transformation to apply to each operation object.
     * @return A new PathItemObject with the transformation applied to all operations.
     */
    private fun PathItemObject.applyToAllOperations(block: (OperationObject) -> OperationObject): PathItemObject {
        return copy(
            get = get?.let { block(it) },
            post = post?.let { block(it) },
            put = put?.let { block(it) },
            delete = delete?.let { block(it) },
            patch = patch?.let { block(it) },
            options = options?.let { block(it) },
            head = head?.let { block(it) },
        )
    }

    /**
     * Filters a parameter to determine if it should be included in the processed schema.
     *
     * @param parameter The parameter to check.
     * @return True if the parameter should be kept, false if it should be filtered out.
     */
    private fun shouldKeepParameter(parameter: Any): Boolean {
        return when (parameter) {
            is ParameterObject -> parameter.name !in filterParams
            is ReferenceObject -> {
                val parameterRefs = filterParams.map { param -> "#/components/parameters/$param" }
                parameter.ref.value !in parameterRefs
            }

            else -> true
        }
    }

    /**
     * Pagination is not listed in the original openapi spec, but is allowed on every 'List' endpoint
     *
     * https://doc.bunq.com/#/pagination
     *
     */
    private fun List<community.flock.kotlinx.openapi.bindings.v3.ParameterOrReferenceObject>.addPaginationParams(
        operation: OperationObject
    ): List<community.flock.kotlinx.openapi.bindings.v3.ParameterOrReferenceObject> =
        if (operation.operationId?.startsWith("List_") != true) {
            this
        } else {
            this + listOf(
                ParameterObject(
                    name = "count",
                    `in` = ParameterLocation.QUERY,
                    required = false,
                    description = "Pagination parameter. The count value can be indicate the number of items requested. The items in the response always less than or equal to the maximum count value specified in the request.",
                    schema = SchemaObject(
                        type = Type.INTEGER,
                        maximum = 200.0
                    )
                ),
                ParameterObject(
                    name = "newer_id",
                    `in` = ParameterLocation.QUERY,
                    required = false,
                    description = "Pagination parameter. The newer_id value can be used to get the next page. The newer_id is always the ID of the last item in the current page. If newer_url is null, there are no more recent items before the current page.",
                    schema = SchemaObject(
                        type = Type.INTEGER,
                    )
                ), ParameterObject(
                    name = "older_id",
                    `in` = ParameterLocation.QUERY,
                    description = "Pagination parameter. The older_id value can be used to get the previous page. The older_id is always the ID of the first item in the current page. If older_url is null, there are no older items after the current page.",
                    required = false,
                    schema = SchemaObject(
                        type = Type.INTEGER,
                    )
                )
            )
        }


    /**
     * Processes an OpenAPI schema by filtering out specified parameters.
     *
     * @param schema The OpenAPI schema as a JSON string.
     * @return The processed OpenAPI schema as a JSON string.
     */
    override fun invoke(schema: String): String {
        // Parse the OpenAPI schema
        val openApi = OpenAPI(Json { ignoreUnknownKeys = true }).decodeFromString(schema)

//        println("$openApi")
        // Process the paths in the schema
        val processedOpenApi = openApi.copy(
            components = openApi.components?.copy(
                schemas = openApi.components?.schemas?.let { schemas ->
                    val processedSchemas = schemas.mapValues { (key, schema) ->
                        when (schema) {
                            is ReferenceObject -> schema
                            is SchemaObject -> {
                                wrapResponse[key]
                                    ?.let { prop ->
                                        SchemaObject(
                                            type = Type.OBJECT,
                                            properties = mapOf(prop to schema)
                                        )
                                    }
                                    ?: schema
                            }
                        }
                    }.toMutableMap()

                    // Create input schemas for CREATE operations
                    createInputSchemas.forEach { (originalKey, inputKey) ->
                        schemas[originalKey]?.let { originalSchema ->
                            if (originalSchema is SchemaObject) {
                                // For scaffolding, create CreateRequestInquiry with all fields as strings
                                val createRequestInquirySchema = SchemaObject(
                                    type = Type.OBJECT,
                                    properties = mapOf(
                                        "amount_inquired" to ReferenceObject(Ref("#/components/schemas/Amount")),
                                        "counterparty_alias" to ReferenceObject(Ref("#/components/schemas/Pointer")),
                                        "description" to SchemaObject(
                                            type = Type.STRING,
                                            description = "The description for the RequestInquiry"
                                        ),
                                        "allow_bunqme" to SchemaObject(
                                            type = Type.BOOLEAN,
                                            description = "Whether or not sending a bunq.me request is allowed"
                                        ),
                                    ),
                                    required = listOf(
                                        "amount_inquired",
                                        "counterparty_alias",
                                        "description",
                                        "allow_bunqme"
                                    ) // No required fields for now
                                )
                                processedSchemas[inputKey] = createRequestInquirySchema
                            }
                        }
                    }

                    processedSchemas
                }
            ),
            paths = openApi.paths.mapValues { (_, pathItem) ->
                pathItem.applyToAllOperations { operation: OperationObject ->
                    val updatedOperation = operation.copy(
                        parameters = operation.parameters?.filter(::shouldKeepParameter)
                            ?.let { it.addPaginationParams(operation) }
                    )

                    val uppdatedOperation =
                        updateRequestBodyType[updatedOperation.operationId]?.let { newRequestBodyReference ->
                            val requestBody = updatedOperation.requestBody
                            println("Updating request body for ${updatedOperation.operationId}: $requestBody")
                            if (requestBody is RequestBodyObject) {
                                updatedOperation.copy(
                                    requestBody = RequestBodyObject(
                                        description = requestBody.description,
                                        required = requestBody.required,
                                        xProperties = requestBody.xProperties,
                                        content = requestBody.content?.mapValues {
                                            it.value.copy(schema = ReferenceObject(Ref("#/components/schemas/$newRequestBodyReference")))

                                        }
                                    ))

                            } else updatedOperation
                        }
                            ?: updatedOperation

                    uppdatedOperation
                }
            }
        )

        // Serialize the processed schema back to JSON
        return OpenAPI.encodeToString(processedOpenApi)
    }
}
