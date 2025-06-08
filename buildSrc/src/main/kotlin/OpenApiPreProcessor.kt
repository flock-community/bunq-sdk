import community.flock.kotlinx.openapi.bindings.v3.OpenAPI
import community.flock.kotlinx.openapi.bindings.v3.OperationObject
import community.flock.kotlinx.openapi.bindings.v3.ParameterObject
import community.flock.kotlinx.openapi.bindings.v3.PathItemObject
import community.flock.kotlinx.openapi.bindings.v3.ReferenceObject
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
     * Processes an OpenAPI schema by filtering out specified parameters.
     *
     * @param schema The OpenAPI schema as a JSON string.
     * @return The processed OpenAPI schema as a JSON string.
     */
    override fun invoke(schema: String): String {
        // Parse the OpenAPI schema
        val openApi = OpenAPI(Json { ignoreUnknownKeys = true }).decodeFromString(schema)

        // Process the paths in the schema
        val processedOpenApi = openApi.copy(
            paths = openApi.paths.mapValues { (_, pathItem) ->
                pathItem.applyToAllOperations { operation ->
                    operation.copy(
                        parameters = operation.parameters?.filter(::shouldKeepParameter)
                    )
                }
            }
        )

        // Serialize the processed schema back to JSON
        return OpenAPI.encodeToString(processedOpenApi)
    }
}
