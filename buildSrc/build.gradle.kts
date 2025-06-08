plugins {
    id("community.flock.wirespec.plugin.gradle") version "0.15.2"
    kotlin("jvm") version "2.1.0"
    kotlin("plugin.serialization") version "2.1.0"
}

repositories {
    mavenCentral()
    mavenLocal()
}

dependencies {
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.0")
    implementation("community.flock.wirespec.compiler:core-jvm:0.15.2")
    implementation("community.flock.kotlinx.openapi.bindings:kotlin-openapi-bindings-jvm:0.0.25")
}
