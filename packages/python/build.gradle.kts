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

    // Workaround for the Wirespec 0.21.1 Python emitter emitting circular sibling imports in model files; remove once fixed.
    // Annotations are lazy (`from __future__ import annotations`), so sibling imports can move below the classes.
    val siblingImport = Regex("""^from \.\w.*$""")
    doLast {
        // Workaround for unescaped quotes in generated annotations, see https://github.com/flock-community/wirespec/issues/715
        output.get().dir("api/generator").asFile.deleteRecursively()
        output.get().dir("api/model").asFileTree.matching { include("*.py"); exclude("__init__.py") }.forEach { file ->
            val (imports, rest) = file.readLines().partition { siblingImport.matches(it) }
            if (imports.isNotEmpty()) file.writeText((rest + imports).joinToString("\n", postfix = "\n"))
        }
    }
}

tasks.register<Exec>("mypy") {
    commandLine("mypy", ".")
}
