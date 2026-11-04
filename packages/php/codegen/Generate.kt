import community.flock.wirespec.compiler.core.FileUri
import community.flock.wirespec.compiler.core.ModuleContent
import community.flock.wirespec.compiler.core.emit.EmitShared
import community.flock.wirespec.compiler.core.emit.PackageName
import community.flock.wirespec.compiler.core.parse.ParseOptions
import community.flock.wirespec.compiler.core.validate.Validator
import community.flock.wirespec.compiler.utils.noLogger
import community.flock.wirespec.emitters.php.PhpEmitter
import community.flock.wirespec.openapi.v3.OpenAPIV3Parser
import java.io.File

/**
 * Generates the PHP client from the (pre-processed) OpenAPI spec: `Generate <spec> <output dir> <package>`.
 * Runs in its own JVM because buildSrc already puts the released Wirespec, which has no PHP emitter, on the build classpath.
 */
fun main(args: Array<String>) {
    val (spec, output, packageName) = args
    val module = ModuleContent(FileUri(spec), File(spec).readText())
    val emitted = Validator.validate(ParseOptions(strict = true), OpenAPIV3Parser.parse(module, true))
        .map { ast -> PhpEmitter(PackageName(packageName), EmitShared(true)).emit(ast, noLogger) }
        .fold({ errors -> error(errors.joinToString { it.message }) }, { it })
    File(output).deleteRecursively()
    emitted.forEach { File(output, it.file).apply { parentFile.mkdirs() }.writeText(it.result) }
    println("Generated ${emitted.size} PHP files in $output")
}
