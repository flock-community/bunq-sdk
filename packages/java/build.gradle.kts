import arrow.core.NonEmptyList
import community.flock.wirespec.compiler.core.emit.JavaEmitter
import community.flock.wirespec.compiler.core.emit.common.EmitShared
import community.flock.wirespec.compiler.core.emit.common.Emitted
import community.flock.wirespec.compiler.core.emit.common.PackageName
import community.flock.wirespec.compiler.core.emit.common.Spacer
import community.flock.wirespec.compiler.core.parse.Endpoint
import community.flock.wirespec.compiler.core.parse.Module
import community.flock.wirespec.compiler.utils.Logger
import community.flock.wirespec.plugin.Format
import community.flock.wirespec.plugin.gradle.ConvertWirespecTask

plugins {
    alias(libs.plugins.wirespec)
    id("java")
}

repositories {
    mavenCentral()
    mavenLocal()
}

dependencies {
    implementation("org.bouncycastle:bcprov-jdk15on:1.70")
    implementation("com.fasterxml.jackson.core:jackson-databind:2.15.0")
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin:${libs.versions.jackson.get()}")
    implementation("com.fasterxml.jackson.datatype:jackson-datatype-jdk8:${libs.versions.jackson.get()}")
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
            srcDirs(
                layout.buildDirectory.dir("generated").get(),
                "src/main/customGenerated"
            )
        }
    }
}
java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(17)
    }
}

tasks.withType<Test> {
    useJUnitPlatform()
}

tasks.register<ConvertWirespecTask>("wirespec") {
    description = "Compile Wirespec to Java"
    output = layout.buildDirectory.dir("generated")
    input = layout.projectDirectory.file("../../openapi.json")
    packageName = "com.bunq.sdk.generated"
    emitterClass = SdkJavaEmitter::class.java
    format = Format.OpenAPIV3
    strict = true
    shared = true
    preProcessor = OpenApiPreProcessor
}

tasks.named("compileJava") {
    dependsOn("wirespec")
}
class SdkJavaEmitter(val packageName: PackageName, emitShared: EmitShared) : JavaEmitter(packageName, emitShared) {
    override fun emit(module: Module, logger: Logger): NonEmptyList<Emitted> {
        return super.emit(module, logger)
            .plus(
                Emitted(
                    "${packageName.toDir()}/Sdk", """
                |package ${packageName.value};
                |
                |import community.flock.wirespec.java.Wirespec;
                |
                |${module.emitEndpointRequest("\n") { (endpoint) -> "import ${packageName.value}.endpoint.${emit(endpoint.identifier)};" }}
                |
                |${module.statements.toList().flatMap { it.importReferences() }.distinctBy { it.value }.joinToString("\n") { "import ${packageName.value}.model.${it.value};" }}   
                |
                |public class Sdk {
                |${Spacer}private final java.util.function.Function<Wirespec.Request<?>, java.util.concurrent.CompletableFuture<Wirespec.Response<?>>> handler;
                |
                |${Spacer}public Sdk(java.util.function.Function<Wirespec.Request<?>, java.util.concurrent.CompletableFuture<Wirespec.Response<?>>> handler) {
                |${Spacer(2)}this.handler = handler;
                |${Spacer}}
                |
                |${Spacer}public <Req extends Wirespec.Request<?>, Res extends Wirespec.Response<?>> java.util.concurrent.CompletableFuture<Res> handle(Req req) {
                |${Spacer(2)}return (java.util.concurrent.CompletableFuture<Res>) this.handler.apply(req);
                |}
                |
                |${module.emitEndpointRequest("\n") { (endpoint, request) -> endpoint.emitMethod(request) }.spacer(1)}
                |}
            """.trimMargin()
                )
            )
        }
        fun Endpoint.emitMethod(request: Endpoint.Request) = """
            |public java.util.concurrent.CompletableFuture<${emit(identifier)}.Response<?>> ${emit(identifier).firstToLower()}(${request.emitSdkInterface(this)}) {
            |${Spacer}var req = new ${emit(identifier)}.Request(${request.paramList(this).joinToString(", ") { emit(it.identifier) }});
            |${Spacer}return handle(req); 
            |}
            |
        """.trimMargin()

    fun Endpoint.Request.emitSdkInterface(endpoint: Endpoint) =
        this.paramList(endpoint).joinToString(", ") { "${it.reference.emit()} ${emit(it.identifier)}" }

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
