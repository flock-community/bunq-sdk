pluginManagement {
    repositories {
        mavenLocal()
        gradlePluginPortal()
    }
}

// npm and python are disabled until their slices are ported to Wirespec 0.21 (no custom emitters anymore).
include(
    "packages:java",
    "packages:kotlin",
)
