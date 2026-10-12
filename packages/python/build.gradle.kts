import community.flock.wirespec.plugin.Format
import community.flock.wirespec.plugin.Language
import community.flock.wirespec.plugin.gradle.ConvertWirespecTask

plugins {
    alias(libs.plugins.wirespec)
}

repositories {
    mavenCentral()
    mavenLocal()
}

tasks.register<ConvertWirespecTask>("wirespec") {
    description = "Compile Wirespec to Python"
    output = layout.projectDirectory.dir("src")
    input = layout.projectDirectory.file("../../openapi.json")
    packageName = "api"
    format = Format.OpenAPIV3
    languages = listOf(Language.Python)
    strict = true
    shared = true
    preProcessor = OpenApiPreProcessor

    // Upstream Wirespec 0.21.1 bug: model files import each other at the top, which fails with a circular import.
    // Annotations are lazy (`from __future__ import annotations`), so sibling imports can move below the classes.
    val siblingImport = Regex("""^from \.\w.*$""")
    doLast {
        // Upstream Wirespec 0.21.1 bug: generator annotations contain unescaped quotes, so the files are not valid Python.
        output.get().dir("api/generator").asFile.deleteRecursively()
        output.get().dir("api/model").asFileTree.matching { include("*.py") }.forEach { file ->
            val (imports, rest) = file.readLines().partition { siblingImport.matches(it) && !file.name.startsWith("__init__") }
            if (imports.isNotEmpty()) file.writeText((rest + imports).joinToString("\n", postfix = "\n"))
        }
    }
}

tasks.register<Exec>("mypy") {
    commandLine("mypy", ".")
}
