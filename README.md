# Bunq SDK

> ⚠️ **Warning**: This repository is not affiliated with Bunq. It is a research project by Flock. For more information,
> please see our [blog post](https://wirespec.io/blog/bunq-sdk).



This repository showcases how four different SDKs (Java, Kotlin, TypeScript/JavaScript, and Python) are generated from a single OpenAPI specification using Wirespec. All projects follow the same structure and build process, demonstrating the power of code generation for maintaining consistent APIs across multiple programming languages.

## Overview

The repository contains:

- A single OpenAPI specification (`openapi.json`) in the root directory
- Four SDK packages in the `packages` directory:
  - Java SDK
  - Kotlin SDK
  - NPM (TypeScript/JavaScript) SDK
  - Python SDK
- Custom build logic in the `buildSrc` directory
- Gradle build configuration for all packages

## How It Works

### OpenAPI Specification

The repository uses a single OpenAPI specification (`openapi.json`) as the source of truth for all SDKs. This ensures that all SDKs have consistent API definitions, models, and endpoints.

### Wirespec

[Wirespec](https://github.com/flock-community/wirespec) is used to generate code from the OpenAPI specification. Wirespec is a language and code generation tool that can generate client libraries for multiple programming languages from a single specification.

Each SDK package uses the Wirespec Gradle plugin to:
1. Read the OpenAPI specification
2. Apply custom pre-processing (via `OpenApiPreProcessor`)
3. Generate code using a custom emitter class
4. Include the generated code in the build

## Requirements

Wirespec 0.21.1 generates the client code in all four packages.

- Kotlin: Kotlin 2.3+, JVM 17+, Wirespec 0.21.x runtime. Bring your own kotlinx-coroutines (the client functions are `suspend`).
- Java: Java 17+.
- TypeScript: Node.js with a global `fetch` (CI uses Node 20), TypeScript 5.
- Python: Python 3.10+ (the generated code uses `match`/`case`).

## Using the SDKs

Each SDK has the same three steps: create a `Config`, call `initContext` to create a session, and create the client from the context. The client is the one Wirespec generates, with one method per bunq operation (camelCase in Kotlin, Java and TypeScript, snake_case in Python).

The client refreshes the session by itself: when bunq answers 403 "Insufficient authentication.", it creates a new session once, retries the request, and shares that refresh between concurrent calls. If the refresh fails, the original 403 is returned.

For install steps, configuration and more examples per language, see:

- [Java](docs/java.md)
- [Kotlin](docs/kotlin.md)
- [TypeScript/npm](docs/typescript.md)
- [Python](docs/python.md)

**Quick Examples:**

Kotlin:
```kotlin
val context = initContext(config)
val client = bunqClient(context)
when (val res = client.readUser(context.userId)) {
    is ReadUser.Response200 -> println(res.body.UserPerson?.legal_name)
    else -> error("Cannot read user")
}
```

Java:
```java
Context context = Context.initContext(config);
Client client = Wirespec.bunqClient(context);
ReadUser.Response<?> res = client.readUser(context.userId()).get();
```

TypeScript:
```typescript
const context = await initContext(config);
const client = bunqClient(context);
const res = await client.readUser({itemId: context.userId});
```

Python:
```python
async def main():
    ctx = await init_context(config)
    client = bunq_client(ctx)
    res = await client.read_user(itemId=ctx.user_id)

asyncio.run(main())
```

## Migrating from 0.x

The packages moved from Wirespec 0.16.3 to 0.21.1 and use the generated client instead of our own `Sdk`/`handler` code.

All languages:

- The `Sdk` class, `handler(...)` and `handle(...)` are removed. Use `bunqClient(initContext(config))` (Kotlin), `Wirespec.bunqClient(Context.initContext(config))` (Java), `bunqClient(await initContext(config))` (TypeScript) or `bunq_client(await init_context(config))` (Python).
- Operation and endpoint names are renamed from the operation ids to camelCase: `rEAD_User(...)` becomes `readUser(...)` and `READ_User.Response200` becomes `ReadUser.Response200` (Python methods: `read_user`).
- Code that refreshed the session itself (checking expiry, or retrying after an error) is no longer needed. The client does it on 403 "Insufficient authentication.".

Kotlin:

- Path parameter `monetaryaccountID` is now `monetaryAccountID`; response header fields `XBunq...` are now `xBunq...`; `toRequest`/`fromResponse` are now `toRawRequest`/`fromRawResponse`.
- Query parameters have no defaults: pass `null` for unused ones. Generated GET/DELETE requests carry `body: Unit`.
- `objectMapper` is `internal`. `serialization` is the non-generic `Wirespec.Serialization`, and raw bodies are `ByteArray`.
- Requires Kotlin 2.3+, JVM 17+ and the Wirespec 0.21.x runtime. The runtime uses Jackson 3 (`tools.jackson`). kotlinx-coroutines is not exposed.

Java:

- Requests used a hardcoded sandbox base URL; they now use `config.bunqServer().baseUrl()`.
- The optional config headers (Cache-Control, language, region, client request id, geolocation) are now sent.

TypeScript:

- The package has an entry point (`main`/`types`/`exports` point to `lib/`), so it can be imported by name. `src/gen` is generated and no longer committed.

Python:

- `init_context` and `refresh_session` are coroutines; sync callers use `asyncio.run(...)`. HTTP goes through `httpx` instead of `requests`.
- Requires Python 3.10+.
- Query parameters are now forwarded (they were dropped before), and only requests with a body are signed.

## Contributing

If you want to modify the SDKs:

1. Update the OpenAPI specification (`openapi.json`) if needed
2. Modify the custom emitters in the build files if you need to change the structure of the generated code
3. Run the build to regenerate the SDKs
4. Test the changes to ensure they work as expected

For the npm package, `src/gen` is generated and not committed: run `./gradlew :packages:npm:wirespec` before `npm run build` or `npm test`.

## License

This project is licensed under the terms of the LICENSE file included in the repository.