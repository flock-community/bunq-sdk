pluginManagement {
    repositories {
        mavenLocal()
        mavenCentral()
        gradlePluginPortal()
    }
}

include(
    "packages:java",
    "packages:kotlin",
    "packages:npm",
    "packages:php",
    "packages:python",
)
