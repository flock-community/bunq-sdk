pluginManagement {
    repositories {
        mavenLocal()
        gradlePluginPortal()
    }
}

// java and npm are disabled until their slices are ported to Wirespec 0.21 (no custom emitters anymore).
include(
    "packages:kotlin",
    "packages:python",
)
