plugins {
    kotlin("jvm") version "2.3.20"
}

repositories {
    mavenLocal()
    mavenCentral()
}

// Only the code generator is Kotlin; the SDK itself is the PHP in src/ and the generated code in gen/.
sourceSets {
    main {
        kotlin.setSrcDirs(listOf("codegen"))
        resources.setSrcDirs(emptyList<String>())
    }
    test {
        kotlin.setSrcDirs(emptyList<String>())
        resources.setSrcDirs(emptyList<String>())
    }
}

dependencies {
    implementation(libs.wirespecPhp.compiler)
    implementation(libs.wirespecPhp.emitter)
    implementation(libs.wirespecPhp.openapi)
}

val spec = layout.projectDirectory.file("../../openapi.json")
val preProcessedSpec = layout.buildDirectory.file("openapi.json")

val preProcessOpenApi = tasks.register("preProcessOpenApi") {
    description = "Applies the OpenApiPreProcessor to the OpenAPI specification"
    inputs.file(spec)
    outputs.file(preProcessedSpec)
    doLast {
        preProcessedSpec.get().asFile.writeText(OpenApiPreProcessor(spec.asFile.readText()))
    }
}

tasks.register<JavaExec>("wirespec") {
    description = "Compile Wirespec to PHP"
    dependsOn(preProcessOpenApi)
    classpath = sourceSets.main.get().runtimeClasspath
    mainClass = "GenerateKt"
    args(preProcessedSpec.get().asFile.path, layout.projectDirectory.dir("gen").asFile.path, "bunq.api")
}
