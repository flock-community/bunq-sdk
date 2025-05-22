pluginManagement {
    repositories {
        mavenLocal()
        gradlePluginPortal()
    }
}

include(
    "packages:kotlin",
    "packages:python",
    "packages:java",
    "packages:npm"
)
