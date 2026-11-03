# bunq-sdk

Four SDKs (Java, Kotlin, TypeScript, Python) under `packages/`, all generated from one OpenAPI spec (`openapi.json`) with Wirespec. To change an SDK, change the spec or `buildSrc/src/main/kotlin/OpenApiPreProcessor.kt` and regenerate.

`packages/python/src/api` and `packages/npm/src/gen` are generated and git-ignored. The Python and npm tests need them, so run `./gradlew :packages:python:wirespec` or `./gradlew :packages:npm:wirespec` first.

CI (`.github/workflows/build.yml`) runs each Python test file by name, so a new Python test file also has to be added there.
