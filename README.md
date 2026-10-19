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

`Context` holds the session token, installation token and `config` (API key and private key); treat a stored context as a secret.

## Session Refresh

The client refreshes the session by itself. When bunq answers 403 "Insufficient authentication." (the response for an expired or deleted session), the client:

1. creates a new session once and retries the request with the new token, signed again;
2. shares that one refresh between concurrent calls, and keeps the new session inside the client, so later calls use the new token.

Keep using the same client instance so that calls share the refreshed session.

If the refresh fails, a warning is logged and the call throws the API exception with status 403 (see [Error Handling](#error-handling)). A 403 for another reason (for example a missing permission), or a 403 with a body that is not JSON, throws the same exception without a refresh.

`Context.refreshSession()` (`refreshSession(context)` in TypeScript and Python) still creates a session by hand and returns a new `Context`. An existing client does not use it; create a new client from the returned context.

## Error Handling

An operation returns a typed response for two statuses only: 200 (`Response200`, the body of the operation) and 400 (`Response400`, whose body is a list `Error[]` where each entry has an `error_description`). A response is typed when it is a 200 whose body is a JSON object with `Response`, or a 400 whose body is a JSON object with `Error`. Everything else throws one exception that carries the status and the body:

| Language | Exception | Import |
| --- | --- | --- |
| Kotlin | `BunqApiException` (unchecked) | `com.bunq.sdk.BunqApiException` |
| Java | `BunqApiException` (unchecked) | `com.bunq.sdk.BunqApiException` |
| TypeScript | `BunqApiError` | `import {BunqApiError} from "bunq-sdk"` |
| Python | `BunqApiError` | `from transport import BunqApiError` |

It has a `status` and a `body` (the full response body as a string). The message is `bunq answered <status>: ` followed by the first 500 characters of the body.

It is thrown for:

- any other status, for example 401, 403, 404, 429, 500 or a gateway 502, 503 or 504;
- a body that is not a JSON object (an HTML page from a proxy, an empty body);
- a 200 without `Response`, or a 400 without `Error` (for example a gateway's `{"message":"Bad Request"}`).

The recommended pattern is an exhaustive `when` (Kotlin), `instanceof` (Java), `if` on `status` (TypeScript) or `match` (Python) over `Response200` and `Response400`, inside a `try` for the exception. See the language pages and the examples below.

- Java: the exception arrives wrapped, in a `CompletionException` when you call `join()` and in an `ExecutionException` when you call `get()`. Check `getCause()`.
- Transport failures (no connection, timeout) throw the exception of the HTTP client.
- `initContext` and `refreshSession` use the same rule. A typed 400 gives `Cannot create installation (status 400): <error_description>` (Kotlin and Java; the step is "create installation", "create device server" or "create session server") or `Installation failed (status 400): <error_description>` (TypeScript and Python; the steps are "Installation failed", "Device server creation failed", "Session server creation failed"). Any other status throws the API exception.

## Quick Examples

Kotlin:
```kotlin
val context = initContext(config)
val client = bunqClient(context)
try {
    when (val res = client.readUser(context.userId)) {
        is ReadUser.Response200 -> println(res.body.UserPerson?.legal_name)
        is ReadUser.Response400 -> error("bunq answered 400: ${res.body.Error?.firstOrNull()?.error_description}")
    }
} catch (e: BunqApiException) {
    println("bunq answered ${e.status}: ${e.body}")
}
```

Java:
```java
Context context = Context.initContext(config);
Client client = Wirespec.bunqClient(context);
try {
    ReadUser.Response<?> res = client.readUser(context.userId()).join();
    if (res instanceof ReadUser.Response200 ok) {
        System.out.println(ok.body().UserPerson().flatMap(UserPerson::legal_name).orElse(null));
    } else if (res instanceof ReadUser.Response400 bad) {
        throw new IllegalStateException(
            bad.body().Error().flatMap(errors -> errors.stream().findFirst()).flatMap(ErrorArray::error_description).orElse(null));
    }
} catch (CompletionException e) {
    if (e.getCause() instanceof BunqApiException api) {
        System.out.println("bunq answered " + api.status() + ": " + api.body());
    } else {
        throw e;
    }
}
```

TypeScript:
```typescript
const context = await initContext(config);
const client = bunqClient(context);
try {
  const res = await client.readUser({itemId: context.userId});
  if (res.status === 200) {
    console.log(res.body.UserPerson?.legal_name);
  } else {
    throw new Error(res.body.Error?.[0]?.error_description);
  }
} catch (e) {
  if (e instanceof BunqApiError) {
    console.log(`bunq answered ${e.status}: ${e.body}`);
  } else {
    throw e;
  }
}
```

Python:
```python
from api.endpoint.ReadUser import Response200 as ReadUserResponse200, Response400 as ReadUserResponse400
from transport import BunqApiError

async def main():
    ctx = await init_context(config)
    client = bunq_client(ctx)
    try:
        res = await client.read_user(itemId=ctx.user_id)
        match res:
            case ReadUserResponse200(body=body):
                print(body.UserPerson.legal_name if body.UserPerson else None)
            case ReadUserResponse400(body=body):
                raise RuntimeError(body.Error[0].error_description if body.Error else None)
    except BunqApiError as e:
        print(f"bunq answered {e.status}: {e.body}")

asyncio.run(main())
```

## Migrating from 0.x

The packages moved from Wirespec 0.16.3 to 0.21.1 and use the generated client instead of our own `Sdk`/`handler` code.

All languages:

- The `Sdk` class, `handler(...)`, `handle(...)` and (TypeScript) `initHandler(...)` are removed. Use `bunqClient(initContext(config))` (Kotlin), `Wirespec.bunqClient(Context.initContext(config))` (Java), `bunqClient(await initContext(config))` (TypeScript) or `bunq_client(await init_context(config))` (Python).
- Operation and endpoint names are renamed from the operation ids to camelCase: `rEAD_User(...)` (Kotlin) or `READ_User` (TypeScript) becomes `readUser(...)`, and `READ_User.Response200` becomes `ReadUser.Response200` (Python methods: `read_user`).
- The path parameter `monetaryaccountID` (Kotlin, Java, Python) or `"monetary-accountID"` (TypeScript) is now `monetaryAccountID`.
- Code that refreshed the session itself (checking expiry, or retrying after an error) is no longer needed. The client does it on 403 "Insufficient authentication.".
- Statuses other than 200 and 400 now throw `BunqApiException` (Kotlin, Java) or `BunqApiError` (TypeScript, Python) with the status and the body. Before they threw `Cannot match response with status: N` without the body.
- A failed session refresh throws that exception with status 403.
- `initContext` and `refreshSession` error messages include the status and bunq's `error_description` (see Error Handling).

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

### Releasing

Kotlin and Java are published through JitPack, configured in `jitpack.yml`.

1. On GitHub, create a release with tag `X.Y.Z` from `main`.
2. JitPack builds `kotlin` and `java` on the first request for that version. Opening `https://jitpack.io/#flock-community/bunq-sdk` does not start a build; clicking "Get it" next to the version or resolving the dependency does.
3. Check the build log:

```text
https://jitpack.io/com/github/flock-community/bunq-sdk/X.Y.Z/build.log
```

## License

This project is licensed under the terms of the LICENSE file included in the repository.
