import arrow.core.NonEmptyList
import community.flock.wirespec.compiler.core.emit.PythonEmitter
import community.flock.wirespec.compiler.core.emit.common.EmitShared
import community.flock.wirespec.compiler.core.emit.common.Emitted
import community.flock.wirespec.compiler.core.emit.common.PackageName
import community.flock.wirespec.compiler.core.parse.Endpoint
import community.flock.wirespec.compiler.core.parse.Module
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
    preProcessor = { it -> it }
}

class SdkPythonEmitter(val packageName: PackageName, emitShared: EmitShared): PythonEmitter(packageName, emitShared) {
    override fun emit(module: Module, logger: community.flock.wirespec.compiler.utils.Logger): NonEmptyList<Emitted> {
        return super.emit(module, logger)
            .let { it + Emitted("${packageName.toDir()}/sdk", """
                |from . import endpoint
                |
                |class Sdk(
                |${module.statements.filterIsInstance<Endpoint>().joinToString(",\n") {endpoint ->  "endpoint.${emit(endpoint.identifier)}.Handler" }.spacer(1)}
                |):
                |
                |  def __init__(self, handler, serialization):
                |    self.handler = handler
                |    self.serialization = serialization
                | 
                |${module.statements.filterIsInstance<Endpoint>().joinToString("\n") {endpoint ->  "def ${emit(endpoint.identifier)}(self, req): return self.handler(self.serialization, endpoint.${emit(endpoint.identifier)}, req)" }.spacer(1)}
            """.trimMargin()) }
    }
}

tasks.register<Exec>("mypy") {
    commandLine("mypy", ".")
}
