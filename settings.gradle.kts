pluginManagement {
    repositories {
        mavenLocal()
        gradlePluginPortal()
    }
}

include(
    "packages:java",
    "packages:kotlin",
    "packages:npm",
    "packages:python",
)
