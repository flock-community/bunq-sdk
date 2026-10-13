# Bunq SDK

> ⚠️ **Warning**: This repository is not affiliated with Bunq. It is a research project by Flock. For more information,
> please see our [blog post](https://wirespec.io/blog/bunq-sdk).



This repository showcases how four different SDKs (Java, Kotlin, TypeScript/JavaScript, and Python) are generated from a single OpenAPI specification using Wirespec. All projects follow the same structure and build process.

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
2. Apply pre-processing (via `OpenApiPreProcessor`)
3. Generate code with Wirespec's own emitter for that language
4. Include the generated code in the build

## Requirements

Wirespec 0.21.1 generates the client code in all four packages.

- Kotlin: Kotlin 2.3+, JVM 17+, Wirespec 0.21.x runtime. Bring your own kotlinx-coroutines (the client functions are `suspend`).
- Java: Java 17+.
- TypeScript: Node.js 18+ (global `fetch`; CI uses Node 20), TypeScript 5.
- Python: Python 3.10+ (the generated code uses `match`/`case`).

## Using the SDKs

Each SDK has the same three steps: create a `Config`, call `initContext` to create a session, and create the client from the context. The client is the one Wirespec generates, with one method per bunq operation (camelCase in Kotlin, Java and TypeScript, snake_case in Python).

To get an API key for the bunq sandbox, create a sandbox user. The request needs no authentication and no headers:

```bash
curl -s -X POST https://public-api.sandbox.bunq.com/v1/sandbox-user-person | jq -r '.Response[0].ApiKey.api_key'
```

The key is in `Response[].ApiKey.api_key` of the response.

For install steps, configuration and more examples per language, see:

- [Java](docs/java.md)
- [Kotlin](docs/kotlin.md)
- [TypeScript/npm](docs/typescript.md)
- [Python](docs/python.md)

## Session Refresh

The client refreshes the session by itself. When bunq answers 403 "Insufficient authentication." (the response for an expired or deleted session), the client:

1. creates a new session once and retries the request with the new token, signed again;
2. shares that one refresh between concurrent calls, and keeps the new session inside the client, so later calls use the new token.

Keep using the same client instance so that calls share the refreshed session.

If the refresh fails, a warning is logged and the transport returns the original 403. The client does not throw: the call returns the typed 403 response (`Response403`, a `ResponseGenericError`; in TypeScript a response with `status === 403`) with the `GenericError` body. A 403 for another reason (for example a missing permission) is returned the same way. See [Error Handling](#error-handling).

`Context.refreshSession()` (`refreshSession(context)` in TypeScript and Python) still creates a session by hand and returns a new `Context`. An existing client does not use it; create a new client from the returned context.

## Error Handling

Every operation returns a typed response for these error statuses: 400, 401, 403, 404, 405, 429, 466, 490, 491 and 500. They all carry the same `GenericError` body, a list `Error[]` where each entry has an `error_description`. `openapi.json` lists only 200 and 400; the build adds the other statuses (see `OpenApiPreProcessor`).

- Kotlin: the error responses are `X.Response400`, `X.Response401`, ... and all implement `X.ResponseGenericError`. A `when` with `is X.Response200` and `is X.ResponseGenericError` is exhaustive.
- Java: the same classes; test with `instanceof X.ResponseGenericError`.
- TypeScript: the response has a `status`; when it is not 200, `body` is a `GenericError`.
- Python: the same classes; match `Response200` and the generic error class `ResponseGenericError`.

Other cases:

- A status that is not in the list (for example a gateway 502, 503 or 504) throws `Cannot match response with status: N` (Kotlin `IllegalStateException`, Java `IllegalStateException`, TypeScript `Error`, Python `Exception`).
- A status of 400 or higher with a non-empty body that is not JSON (for example an HTML page from a proxy) throws `bunq answered N with a non-JSON body: ` followed by the first 200 characters of the body.
- A JSON body with neither `Response` nor `Error` throws `Invalid bunq response: neither Response nor Error`.
- Transport failures (no connection, timeout) throw the exception of the HTTP client.
- `initContext` and `refreshSession` throw `Cannot <step> (status N): <error_description>`, where the step is "create installation", "create device server" or "create session server" (TypeScript: "Installation failed", "Device server creation failed", "Session server creation failed"; Python: the same wording as TypeScript).

## Quick Examples

Kotlin:
```kotlin
val context = initContext(config)
val client = bunqClient(context)
when (val res = client.readUser(context.userId)) {
    is ReadUser.Response200 -> println(res.body.UserPerson?.legal_name)
    is ReadUser.ResponseGenericError -> error("${res.status}: ${res.body.Error?.firstOrNull()?.error_description}")
}
```

Java:
```java
Context context = Context.initContext(config);
Client client = Wirespec.bunqClient(context);
ReadUser.Response<?> res = client.readUser(context.userId()).get();
if (res instanceof ReadUser.Response200 ok) {
    System.out.println(ok.body().UserPerson().flatMap(UserPerson::legal_name).orElse(null));
} else if (res instanceof ReadUser.ResponseGenericError e) {
    throw new IllegalStateException(e.status() + ": " + e.body().Error().orElseThrow().get(0).error_description().orElse(null));
}
```

TypeScript:
```typescript
const context = await initContext(config);
const client = bunqClient(context);
const res = await client.readUser({itemId: context.userId});
if (res.status === 200) {
  console.log(res.body.UserPerson?.legal_name);
} else {
  throw new Error(`${res.status}: ${res.body.Error?.[0]?.error_description}`);
}
```

Python:
```python
async def main():
    ctx = await init_context(config)
    client = bunq_client(ctx)
    res = await client.read_user(itemId=ctx.user_id)
    match res:
        case ReadUserResponse200(body=body):
            print(body.UserPerson.legal_name if body.UserPerson else None)
        case ReadUserResponseGenericError(status=status, body=body):
            raise RuntimeError(f"{status}: {body.Error[0].error_description if body.Error else None}")

asyncio.run(main())
```

## Migrating from 0.x

The packages moved from Wirespec 0.16.3 to 0.21.1 and use the generated client instead of our own `Sdk`/`handler` code.

All languages:

- The `Sdk` class, `handler(...)`, `handle(...)` and (TypeScript) `initHandler(...)` are removed. Use `bunqClient(initContext(config))` (Kotlin), `Wirespec.bunqClient(Context.initContext(config))` (Java), `bunqClient(await initContext(config))` (TypeScript) or `bunq_client(await init_context(config))` (Python).
- Operation and endpoint names are renamed from the operation ids to camelCase: `rEAD_User(...)` (Kotlin) or `READ_User` (TypeScript) becomes `readUser(...)`, and `READ_User.Response200` becomes `ReadUser.Response200` (Python methods: `read_user`).
- The path parameter `monetaryaccountID` (Kotlin, Java, Python) or `"monetary-accountID"` (TypeScript) is now `monetaryAccountID`.
- Code that refreshed the session itself (checking expiry, or retrying after an error) is no longer needed. The client does it on 403 "Insufficient authentication.".
- Every response type has 10 error subtypes (400, 401, 403, 404, 405, 429, 466, 490, 491, 500) instead of only 400. Code that handled only 200 and 400 must handle the rest: Kotlin `is X.ResponseGenericError` (a `when` with only `Response200` and `Response400` no longer compiles), Java `instanceof X.ResponseGenericError`, TypeScript `status !== 200`, Python `case _` or the `ResponseGenericError` class.
- The per-operation error body types (`XxxNNNResponseBody`) are replaced by the shared `GenericError`.
- A failed session refresh returns a typed `Response403` (TypeScript: status 403) instead of throwing.
- Statuses outside the list above (502, 503, 504) still throw `Cannot match response with status: N`.
- The jars are about 80% larger (Java 16 to 30 MB, Kotlin 23 to 41 MB).

Kotlin:

- Response header fields `XBunq...` are now `xBunq...`; `toRequest`/`fromResponse` are now `toRawRequest`/`fromRawResponse`.
- Query parameters have no defaults: pass `null` for unused ones. Generated GET/DELETE requests carry `body: Unit`.
- `objectMapper` is `internal`. `serialization` is the non-generic `Wirespec.Serialization`, and raw bodies are `ByteArray`.
- Requires Kotlin 2.3+, JVM 17+ and the Wirespec 0.21.x runtime. The runtime uses Jackson 3 (`tools.jackson`). kotlinx-coroutines is not exposed.

Java:

- `Wirespec.serialization` is the non-generic `Serialization`, and raw request and response bodies are `Optional<byte[]>`.
- Requests used a hardcoded sandbox base URL; they now use `config.bunqServer().baseUrl()`.
- The optional config headers (Cache-Control, language, region, client request id, geolocation) are now sent.

TypeScript:

- The package has an entry point (`main`/`types`/`exports` point to `lib/`), so it can be imported by name. `src/gen` is generated and no longer committed.

Python:

- `init_context`, `refresh_session` and `transport.send` are coroutines; sync callers use `asyncio.run(...)`. HTTP goes through `httpx` instead of `requests`.
- Requires Python 3.10+.
- Query parameters are now forwarded (they were dropped before), and only requests with a body are signed.

## Contributing

If you want to modify the SDKs:

1. Update the OpenAPI specification (`openapi.json`) if needed
2. Change `buildSrc/src/main/kotlin/OpenApiPreProcessor.kt` if the spec needs pre-processing before generation. The code itself is generated by Wirespec's own emitters
3. Run the build to regenerate the SDKs
4. Test the changes to ensure they work as expected

For the npm package, `src/gen` is generated and not committed: run `./gradlew :packages:npm:wirespec` before `npm run build` or `npm test`.

## License

This project is licensed under the terms of the LICENSE file included in the repository.