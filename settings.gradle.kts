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
    "packages:python",
)
