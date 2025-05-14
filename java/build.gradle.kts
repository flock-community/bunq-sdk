import community.flock.wirespec.plugin.Format
import community.flock.wirespec.plugin.Language
import community.flock.wirespec.plugin.gradle.ConvertWirespecTask

plugins {
    alias(libs.plugins.wirespec)
    id("java")
}

repositories {
    mavenCentral()
    mavenLocal()
}

dependencies{
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

tasks.register<ConvertWirespecTask>("wirespec-java") {
    description = "Compile Wirespec to Java"
    output = layout.buildDirectory.dir("generated")
    input = layout.projectDirectory.file("../openapi.json")
    packageName = "com.bunq.sdk.generated"
    languages = listOf(Language.Java)
    format = Format.OpenAPIV3
    strict = true
    shared = true
}

tasks.named("compileJava") {
    dependsOn("wirespec-java")
}