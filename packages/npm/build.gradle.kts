import arrow.core.NonEmptyList
import community.flock.wirespec.compiler.core.emit.TypeScriptEmitter
import community.flock.wirespec.compiler.core.emit.common.EmitShared
import community.flock.wirespec.compiler.core.emit.common.Emitted
import community.flock.wirespec.compiler.core.emit.common.Spacer
import community.flock.wirespec.compiler.core.parse.Endpoint
import community.flock.wirespec.compiler.core.parse.Module
import community.flock.wirespec.plugin.Format
import community.flock.wirespec.plugin.gradle.ConvertWirespecTask
import community.flock.wirespec.compiler.utils.Logger

plugins {
    alias(libs.plugins.wirespec)
}

group = "community.flock.wirespec.example.gradle"
version = libs.versions.wirespec.get()

repositories {
    mavenCentral()
    mavenLocal()
}

buildscript {
    dependencies {
        classpath(libs.wirespec.compiler)
    }
}

tasks.register<ConvertWirespecTask>("wirespec") {
    output = layout.projectDirectory.dir("src/gen")
    input = layout.projectDirectory.file("../../openapi.json")
    packageName = "api"
    emitterClass = SdkTypeScriptEmitter::class.java
    format = Format.OpenAPIV3
    strict = true
    shared = true
    preProcessor = OpenApiPreProcessor
}

class SdkTypeScriptEmitter(emitShared: EmitShared) : TypeScriptEmitter(emitShared) {
    override fun emit(module: Module, logger: Logger): NonEmptyList<Emitted> {
        return super.emit(module, logger) +
                Emitted("Sdk", """
                |import {Wirespec} from "./Wirespec"
                |
                |
                |${module.emitEndpointRequest("\n") { (endpoint) -> "import {${endpoint.identifier.value}} from \"./endpoint/${endpoint.identifier.value}\"" }}
                |
                |${module.statements.toList().flatMap { it.importReferences() }.distinctBy { it.value }.joinToString("\n") { "import {${it.value}} from \"./model/${it.value}\"" }}
                |
                |type Handler = <REQ extends Wirespec.Request<unknown>, RES extends Wirespec.Response<unknown>> (client: Wirespec.Client<REQ, RES>, req:REQ) => Promise<RES>
                |
                |export const Sdk = (handler: Handler) => ({
                |${module.emitEndpointRequest("\n") { (endpoint, request) -> emitFunction(endpoint, request) }.spacer(1)}
                |})
                |
            """.trimMargin())
    }

    fun Endpoint.Request.emitSdkInterface(endpoint: Endpoint) =
        this.paramList(endpoint).joinToString(", ") { "${emit(it.identifier)}: ${it.reference.emit()}" }

    fun emitFunction(endpoint: Endpoint, request: Endpoint.Request) = """
        |${endpoint.identifier.value}: async (props: {${request.emitSdkInterface(endpoint)}}) => {
        |${Spacer}const req = ${endpoint.identifier.value}.request(${request.paramList(endpoint).takeIf { it.isNotEmpty() }?.let { "props" }.orEmpty()})
        |${Spacer}return  handler(${endpoint.identifier.value}.client, req)
        |},
    """.trimMargin()

    fun Module.emitEndpointRequest(separator: CharSequence, emit: (Pair<Endpoint, Endpoint.Request>) -> String) =
        statements
            .filterIsInstance<Endpoint>()
            .flatMap { endpoint -> endpoint.requests.map { request -> Pair(endpoint, request) } }
            .joinToString(separator) { endpointRequest -> emit(endpointRequest) }
}
