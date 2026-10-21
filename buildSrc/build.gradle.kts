plugins {
    id("community.flock.wirespec.plugin.gradle") version "0.22.4"
    kotlin("jvm") version "2.3.20"
    kotlin("plugin.serialization") version "2.3.20"
}

repositories {
    mavenCentral()
    mavenLocal()
    // JitPack replaces mavenCentral() with a Google mirror that lags behind Maven Central; the Plugin Portal also serves Wirespec
    gradlePluginPortal()
}

dependencies {
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.0")
    implementation("community.flock.wirespec.compiler:core-jvm:0.22.4")
}

dependencies {
    testImplementation(kotlin("test-junit5"))
}

tasks.test {
    useJUnitPlatform()
}
