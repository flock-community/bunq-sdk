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

tasks.register<ConvertWirespecTask>("wirespec") {
    description = "Compile Wirespec to TypeScript"
    output = layout.projectDirectory.dir("src/gen")
    input = layout.projectDirectory.file("../../openapi.json")
    packageName = "api"
    format = Format.OpenAPIV3
    language = Language.TypeScript
    strict = true
    shared = true
    preProcessor = OpenApiPreProcessor
}
