# bunq-sdk

Five SDKs (Java, Kotlin, TypeScript, Python, PHP) under `packages/`, all generated from one OpenAPI spec (`openapi.json`) with Wirespec. To change an SDK, change the spec or `buildSrc/src/main/kotlin/OpenApiPreProcessor.kt` and regenerate.

`packages/python/src/api`, `packages/npm/src/gen` and `packages/php/gen` are generated and git-ignored. The Python, npm and PHP tests need them, so run `./gradlew :packages:python:wirespec`, `./gradlew :packages:npm:wirespec` or `./gradlew :packages:php:wirespec` first.

The PHP emitter is not in a Wirespec release yet: `:packages:php:wirespec` runs the Wirespec `0.0.0-SNAPSHOT` compiler from Maven Local (see `docs/php.md` for how to publish it), and the `build-php` CI job builds Wirespec from source first.

CI (`.github/workflows/build.yml`) runs each Python test file by name, so a new Python test file also has to be added there.
