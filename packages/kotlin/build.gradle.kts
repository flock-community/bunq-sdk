import community.flock.wirespec.plugin.Format
import community.flock.wirespec.plugin.Language
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
    implementation("tools.jackson.core:jackson-databind:3.2.3")
    implementation("tools.jackson.module:jackson-module-kotlin:3.2.3")
    implementation("community.flock.wirespec.integration:jackson:${libs.versions.wirespec.get()}")
    api("community.flock.wirespec.integration:wirespec:${libs.versions.wirespec.get()}")
    implementation("io.github.oshai:kotlin-logging-jvm:8.0.4")
    implementation("org.slf4j:slf4j-api:2.0.17")
    implementation("org.jetbrains.kotlin:kotlin-reflect:2.3.20")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.10.1")
    testImplementation("org.jetbrains.kotlin:kotlin-test-junit5:2.3.20")
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.10.1")
    testRuntimeOnly("org.slf4j:slf4j-simple:2.0.17")
}

sourceSets {
    main {
        java {
            srcDir("${layout.buildDirectory.get()}/generated/wirespec")
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
    output = layout.buildDirectory.dir("generated/wirespec")
    input = layout.projectDirectory.file("../../openapi.json")
    packageName = "com.bunq.sdk.generated"
    format = Format.OpenAPIV3
    languages = listOf(Language.Kotlin)
    strict = true
    shared = false
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
