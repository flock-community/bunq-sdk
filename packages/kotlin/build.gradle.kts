import community.flock.wirespec.emitters.kotlin.KotlinEmitter
import community.flock.wirespec.compiler.core.emit.EmitShared
import arrow.core.NonEmptyList
import community.flock.wirespec.compiler.core.emit.Emitted
import community.flock.wirespec.compiler.core.emit.importReferences
import community.flock.wirespec.compiler.core.emit.paramList
import community.flock.wirespec.compiler.core.emit.spacer
import community.flock.wirespec.compiler.core.emit.PackageName
import community.flock.wirespec.compiler.core.parse.ast.Endpoint
import community.flock.wirespec.compiler.core.parse.ast.Module
import community.flock.wirespec.plugin.Format
import community.flock.wirespec.plugin.gradle.ConvertWirespecTask

plugins {
    alias(libs.plugins.wirespec)
    kotlin("jvm") version "2.3.20"
    `java-library`
    `maven-publish`
}

repositories {
    mavenCentral()
    mavenLocal()
}

dependencies {
    implementation("org.bouncycastle:bcprov-jdk15on:1.70")
    api("tools.jackson.core:jackson-databind:3.2.3")
    implementation("tools.jackson.module:jackson-module-kotlin:3.2.3")
    implementation("community.flock.wirespec.integration:jackson:${libs.versions.wirespec.get()}")
    api("community.flock.wirespec.integration:wirespec:${libs.versions.wirespec.get()}")
    implementation("io.github.oshai:kotlin-logging-jvm:8.0.4")
    implementation("org.slf4j:slf4j-api:2.0.17")
    implementation("org.jetbrains.kotlin:kotlin-reflect:2.3.20")
    api("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.10.1")
    testImplementation("org.jetbrains.kotlin:kotlin-test-junit5:2.1.20")
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.10.1")
    testRuntimeOnly("org.slf4j:slf4j-simple:2.0.17")
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
    preProcessor = OpenApiPreProcessor
}

tasks.named("compileKotlin") {
    dependsOn("wirespec")
}

val sourcesJar by tasks.registering(Jar::class) {
    archiveClassifier.set("sources")
    from(sourceSets.main.get().allSource)
    dependsOn("wirespec", "compileJava")
}

publishing {
    publications {
        create<MavenPublication>("mavenKotlin") {
            from(components["java"])
            artifact(sourcesJar.get())
            groupId = project.group.toString()
            artifactId = project.name
            version = project.version.toString()
        }
    }
    repositories {
        mavenLocal()
    }
}


class SdkKotlinEmitter(packageName: PackageName, emitShared: EmitShared) : KotlinEmitter(packageName, emitShared) {
    override fun emit(module: Module, logger: community.flock.wirespec.compiler.utils.Logger): NonEmptyList<Emitted> {
        return super.emit(module, logger) +
            Emitted("${packageName.toDir()}/Sdk", """
                |package ${packageName.value}
                |
                |import community.flock.wirespec.kotlin.Wirespec
                |
                |${module.emitEndpointRequest("\n") { (endpoint) -> "import ${packageName.value}.endpoint.${emit(endpoint.identifier)}" }}
                |
                |${module.statements.toList().flatMap { it.importReferences() }.distinctBy { it.value }.joinToString("\n") { "import ${packageName.value}.model.${it.value}" }}
                |
                |class Sdk(val handler: (Wirespec.Request<*>) -> Wirespec.Response<*> ){
                |${module.emitEndpointRequest("\n") { (endpoint, request) -> emitFunction(endpoint, request) }.spacer(1)}
                |}
                |
            """.trimMargin())
    }

    fun Endpoint.Request.emitSdkInterface(endpoint: Endpoint) =
        this.paramList(endpoint).joinToString(", ") { "${emit(it.identifier)}: ${it.reference.emit()}" }

    fun emitFunction(endpoint: Endpoint, request: Endpoint.Request) = """
        |suspend fun ${emit(endpoint.identifier).firstToLower()}(${request.emitSdkInterface(endpoint)}) = 
        |   ${emit(endpoint.identifier)}.Request${request.paramList(endpoint).takeIf { it.size > 0 }?.joinToString(", ", "(", ")") { emit(it.identifier) }.orEmpty()}
        |     .let{req -> handler(req) as ${emit(endpoint.identifier)}.Response<*> }
    """.trimMargin()

    fun Module.emitEndpointRequest(separator: CharSequence, emit: (Pair<Endpoint, Endpoint.Request>) -> String) =
        statements
            .filterIsInstance<Endpoint>()
            .flatMap { endpoint -> endpoint.requests.map { request -> Pair(endpoint, request) } }
            .joinToString(separator) { endpointRequest -> emit(endpointRequest) }
}
