import community.flock.wirespec.plugin.Format
import community.flock.wirespec.plugin.Language
import community.flock.wirespec.plugin.gradle.ConvertWirespecTask

plugins {
    alias(libs.plugins.wirespec)
    id("java-library")
    `maven-publish`
}

repositories {
    mavenCentral()
    mavenLocal()
}

dependencies {
    implementation("org.bouncycastle:bcprov-jdk15on:1.70")
    api("com.fasterxml.jackson.core:jackson-databind:${libs.versions.jackson.get()}")
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin:${libs.versions.jackson.get()}")
    implementation("com.fasterxml.jackson.datatype:jackson-datatype-jdk8:${libs.versions.jackson.get()}")
    implementation("community.flock.wirespec.integration:jackson:${libs.versions.wirespec.get()}")
    api("community.flock.wirespec.integration:wirespec:${libs.versions.wirespec.get()}")
    implementation("org.jetbrains.kotlin:kotlin-reflect:2.3.20")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.10.1")
    testImplementation("org.jetbrains.kotlin:kotlin-test-junit5:2.3.20")
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.10.1")
}

sourceSets {
    main {
        java {
            srcDirs(
                layout.buildDirectory.dir("generated/wirespec").get(),
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

tasks.withType<JavaCompile> {
    options.isFork = true
    options.forkOptions.memoryMaximumSize = "2g"
}

tasks.withType<Test> {
    useJUnitPlatform()
}

tasks.register<ConvertWirespecTask>("wirespec") {
    description = "Compile Wirespec to Java"
    output = layout.buildDirectory.dir("generated/wirespec")
    input = layout.projectDirectory.file("../../openapi.json")
    packageName = "com.bunq.sdk.generated"
    format = Format.OpenAPIV3
    languages = listOf(Language.Java)
    strict = true
    shared = false
    preProcessor = OpenApiPreProcessor
}

tasks.named("compileJava") {
    dependsOn("wirespec")
}


val sourcesJar by tasks.registering(Jar::class) {
    archiveClassifier.set("sources")
    from(sourceSets.main.get().allSource)
    dependsOn("wirespec", "compileJava")
}

publishing {
    publications {
        create<MavenPublication>("mavenJava") {
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
