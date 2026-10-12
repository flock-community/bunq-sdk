import arrow.core.NonEmptyList
import community.flock.wirespec.compiler.core.emit.EmitShared
import community.flock.wirespec.compiler.core.emit.Emitted
import community.flock.wirespec.compiler.core.emit.PackageName
import community.flock.wirespec.compiler.core.emit.importReferences
import community.flock.wirespec.compiler.core.emit.paramList
import community.flock.wirespec.compiler.core.emit.spacer
import community.flock.wirespec.emitters.python.PythonEmitter
import community.flock.wirespec.compiler.core.parse.ast.Endpoint
import community.flock.wirespec.compiler.core.parse.ast.Module
import community.flock.wirespec.plugin.Format
import community.flock.wirespec.plugin.Language
import community.flock.wirespec.plugin.gradle.ConvertWirespecTask

plugins {
    alias(libs.plugins.wirespec)
}

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
    output = layout.projectDirectory.dir("src")
    input = layout.projectDirectory.file("../../openapi.json")
    packageName = "api"
    emitterClass = SdkPythonEmitter::class.java
    format = Format.OpenAPIV3
    strict = true
    shared = true
    preProcessor = OpenApiPreProcessor
}

class SdkPythonEmitter(val sdkPackageName: PackageName, emitShared: EmitShared): PythonEmitter(sdkPackageName, emitShared) {
    override fun emit(module: Module, logger: community.flock.wirespec.compiler.utils.Logger): NonEmptyList<Emitted> {
        return super.emit(module, logger)
            .let { it + Emitted("${sdkPackageName.toDir()}/sdk", """
                |from . import endpoint
                |
                |from typing import List, Optional
                |
                |${module.statements.toList().flatMap { it.importReferences() }.distinctBy { it.value }.joinToString("\n") { "from .model.${it.value} import ${it.value}" }}
                |
                |class Sdk():
                |
                |  def __init__(self, handler, serialization):
                |    self.handler = handler
                |    self.serialization = serialization
                |
                |${module.emitEndpointRequest("\n") { (endpoint, request) -> emitFunction(endpoint, request) }.spacer(1)}
                |
            """.trimMargin()) }
    }

    fun Endpoint.Request.emitSdkInterface(endpoint: Endpoint) =
        this.paramList(endpoint).joinToString(", ") { "${emit(it.identifier)}: ${it.reference.emit()}" }

    fun emitFunction(endpoint: Endpoint, request: Endpoint.Request) = """
        |def ${emit(endpoint.identifier)}(self, ${request.emitSdkInterface(endpoint)}):
        |   req = endpoint.${emit(endpoint.identifier)}.Request${request.paramList(endpoint).takeIf { it.size > 0 }?.joinToString(", ", "(", ")") { emit(it.identifier) }.orEmpty()}
        |   return self.handler(endpoint.${emit(endpoint.identifier)}, req)
    """.trimMargin()

    fun Module.emitEndpointRequest(separator: CharSequence, emit: (Pair<Endpoint, Endpoint.Request>) -> String) =
        statements
            .filterIsInstance<Endpoint>()
            .flatMap { endpoint -> endpoint.requests.map { request -> Pair(endpoint, request) } }
            .joinToString(separator) { endpointRequest -> emit(endpointRequest) }
}

tasks.register<Exec>("mypy") {
    commandLine("mypy", ".")
}
