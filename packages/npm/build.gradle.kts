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

    // Wirespec 0.21.1 emits validate functions that read capitalised fields (Id, Error, UserPerson) without `obj.`,
    // which does not type-check. The functions are unused by the SDK, so only those files are excluded from type checking.
    val bareFieldAccess = Regex("""(?<!\w)(?<!obj\.)[A-Z]\w* != null""")
    doLast {
        output.get().asFileTree.matching { include("model/*.ts") }.forEach { file ->
            val text = file.readText()
            if (bareFieldAccess.containsMatchIn(text)) file.writeText("// @ts-nocheck\n$text")
        }
    }
}
