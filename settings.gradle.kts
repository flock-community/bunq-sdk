pluginManagement {
    repositories {
        mavenLocal()
        gradlePluginPortal()
    }
}

// java, npm and python are disabled until their slices are ported to Wirespec 0.21 (no custom emitters anymore).
include(
    "packages:kotlin",
)
