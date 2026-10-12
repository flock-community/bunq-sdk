pluginManagement {
    repositories {
        mavenLocal()
        gradlePluginPortal()
    }
}

// python is disabled until its slice is ported to Wirespec 0.21 (no custom emitters anymore).
include(
    "packages:java",
    "packages:kotlin",
    "packages:npm",
)
