import arrow.core.NonEmptyList
import community.flock.wirespec.compiler.core.emit.KotlinEmitter
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
    kotlin("jvm") version "2.1.0"
}

group = "community.flock.wirespec.example.gradle"
version = libs.versions.wirespec.get()

repositories {
    mavenCentral()
    mavenLocal()
}

dependencies{
    implementation("org.bouncycastle:bcprov-jdk15on:1.70")
    implementation("com.fasterxml.jackson.core:jackson-databind:2.15.0")
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin:2.18.+")
    implementation("community.flock.wirespec.integration:jackson:${libs.versions.wirespec.get()}")
    implementation("community.flock.wirespec.integration:wirespec:${libs.versions.wirespec.get()}")
    implementation("org.jetbrains.kotlin:kotlin-reflect:2.1.0")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.10.1")
    testImplementation("org.jetbrains.kotlin:kotlin-test-junit5:2.1.20")
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.10.1")

}

sourceSets {
    main {
        java {
            srcDir("${layout.buildDirectory.get()}/generated")
        }
    }
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(17)
    }
}

kotlin {
    compilerOptions {
        freeCompilerArgs.addAll("-Xjsr305=strict")
    }
}

tasks.withType<Test> {
    useJUnitPlatform()
}

tasks.register<ConvertWirespecTask>("wirespec") {
    description = "Compile Wirespec to Kotlin"
    output = layout.buildDirectory.dir("generated")
    input = layout.projectDirectory.file("../../openapi.json")
    packageName = "com.bunq.sdk.generated"
    emitterClass = SdkKotlinEmitter::class.java
    format = Format.OpenAPIV3
    strict = true
    shared = true
}

tasks.named("compileKotlin") {
    dependsOn("wirespec")
}

class SdkKotlinEmitter(val packageName: PackageName, emitShared: EmitShared): KotlinEmitter(packageName, emitShared) {
    override fun emit(module: Module, logger: community.flock.wirespec.compiler.utils.Logger): NonEmptyList<Emitted> {
        return super.emit(module, logger)
            .let { it + Emitted("${packageName.toDir()}/Sdk", """
                |package ${packageName.value}
                |
                |import community.flock.wirespec.kotlin.Wirespec
                |
                |${module.emitEndpoint("\n"){endpoint ->  "import ${packageName.value}.endpoint.${emit(endpoint.identifier)}" }}
                |
                |class Sdk(val handler: (Wirespec.Request<*>) -> Wirespec.Response<*> ): ${module.emitEndpoint(","){endpoint ->  "${emit(endpoint.identifier)}.Handler" }}{
                |${module.emitEndpoint("\n"){endpoint ->  "override suspend fun ${emit(endpoint.identifier).firstToLower()}(req :${emit(endpoint.identifier)}.Request) = handler(req) as ${emit(endpoint.identifier)}.Response<*>" }.spacer(1)}
                |}
                |
            """.trimMargin()) }
    }

    fun Module.emitEndpoint(separator: CharSequence, emit:(Endpoint) -> String) = statements
        .filterIsInstance<Endpoint>()
        .joinToString(separator){emit(it)}
}


