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
    description = "Compile Wirespec to TypeScript"
    output = layout.projectDirectory.dir("src/gen")
    input = layout.projectDirectory.file("../../openapi.json")
    packageName = "api"
    format = Format.OpenAPIV3
    languages = listOf(Language.TypeScript)
    strict = true
    shared = true
    preProcessor = OpenApiPreProcessor

    // Upstream Wirespec 0.22.4 bug: TypeScript validators read capitalised fields (Id, Error, Response, Pagination) without `obj.`; the validators are unused, so type checking is skipped for those files.
    val bareFieldAccess = Regex("""(?<!\w)(?<!obj\.)[A-Z]\w* != null|\.\.\.Response\.flatMap""")
    doLast {
        // Upstream Wirespec 0.22.4 bug: generator annotations contain unescaped quotes, so the files are not valid TypeScript.
        output.get().dir("generator").asFile.deleteRecursively()
        output.get().asFileTree.matching { include("model/*.ts") }.forEach { file ->
            val text = file.readText()
            if (bareFieldAccess.containsMatchIn(text)) file.writeText("// @ts-nocheck\n$text")
        }
    }
}
