import community.flock.wirespec.plugin.Format
import community.flock.wirespec.plugin.Language
import community.flock.wirespec.plugin.gradle.ConvertWirespecTask

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

tasks.register<ConvertWirespecTask>("wirespec-python") {
    description = "Compile Wirespec to Python"
    group = "Wirespec compile"
    output = layout.projectDirectory.dir("src")
    input = layout.projectDirectory.file("../openapi.json")
    packageName = "api"
    languages = listOf(Language.Python)
    format = Format.OpenAPIV3
    strict = true
    shared = true
}
