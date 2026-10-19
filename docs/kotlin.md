# Kotlin SDK

## Requirements

- Kotlin 2.3+ and JVM 17+
- Wirespec 0.21.x runtime (a consumer that uses Wirespec itself must use 0.21.x as well, because both share one runtime on the classpath)
- kotlinx-coroutines in your own project: the client functions are `suspend`
- Spring Boot 3.x: the SDK uses Jackson 3 (`tools.jackson`), which needs `com.fasterxml.jackson.core:jackson-annotations` 2.20 or later. Spring Boot 3's dependency management pins an older 2.x and the app fails at startup with `ClassNotFoundException` (for example `JsonSerializeAs`). Raise the Jackson BOM version in your build:

```kotlin
extra["jackson-bom.version"] = "2.22.0"
```

## Install

Add the JitPack repository and depend on a release tag. The published artifacts of 0.0.3 and earlier have the old `Sdk`/`handler` API; the client described here ships from 0.1.0.

```kotlin
repositories {
    maven("https://jitpack.io")
    mavenCentral()
}

dependencies {
    implementation("com.github.flock-community.bunq-sdk:kotlin:0.1.0")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.10.1")
}
```

To build from source instead, publish the package to your local Maven repository, add `mavenLocal()` to `repositories` and depend on `com.github.flock-community.bunq-sdk:kotlin:0.0.1-SNAPSHOT`:

```bash
./gradlew :packages:kotlin:publishToMavenLocal
```

## Creating a Context

```kotlin
import com.bunq.sdk.BUNQ_SANDBOX_SERVER
import com.bunq.sdk.BunqSigningKeysGenerator
import com.bunq.sdk.Config
import com.bunq.sdk.Context
import com.bunq.sdk.initContext

val config = Config(
    bunqServer = BUNQ_SANDBOX_SERVER,
    serviceName = "MyApp",
    apiKey = "your-api-key",
    signingKeys = BunqSigningKeysGenerator.generateBunqSigningKeys(),
)
val context: Context = initContext(config)
```

`generateBunqSigningKeys()` creates a new key pair on every call. To keep the same keys across restarts, use `generateBunqSigningKeys(privateKeyFile, publicKeyFile)`, which reuses existing files or writes new ones, or build `SigningKeys.FromPem(privateKeyAsPem, publicKeyAsPem)` from stored PEM strings.

## Creating the Client and Calling an Endpoint

`bunqClient(context)` returns the client that Wirespec generates. Its methods are `suspend` functions named after the operation id in camelCase (`readUser`, `listAllMonetaryAccountBankForUser`). Query parameters have no defaults: pass `null` for the ones you do not use. To call a `suspend` method from non-suspending code, wrap it in `runBlocking { }` (kotlinx-coroutines).

```kotlin
import com.bunq.sdk.bunqClient
import com.bunq.sdk.generated.endpoint.ListAllMonetaryAccountBankForUser
import com.bunq.sdk.generated.endpoint.ReadUser

suspend fun readLegalName(context: Context): String? {
    val client = bunqClient(context)
    return when (val res = client.readUser(context.userId)) {
        is ReadUser.Response200 -> res.body.UserPerson?.legal_name
        is ReadUser.Response400 -> error("bunq answered 400: ${res.body.Error?.firstOrNull()?.error_description}")
    }
}

suspend fun listAccountNames(context: Context): List<String?> {
    val client = bunqClient(context)
    return when (val res = client.listAllMonetaryAccountBankForUser(context.userId, null, null, null)) {
        is ListAllMonetaryAccountBankForUser.Response200 -> res.body.map { it.display_name }
        is ListAllMonetaryAccountBankForUser.Response400 -> error("Cannot list monetary accounts: ${res.body.Error?.firstOrNull()?.error_description}")
    }
}
```

## Session Refresh

See [Session Refresh in the README](../README.md#session-refresh) for how the client refreshes the session, what happens when the refresh fails (the call throws `BunqApiException` with status 403), and the manual refresh.

The shared refresh is guarded by a `Mutex`, and the refresh-failure warning is logged through kotlin-logging (see Logging). Keep using the same `bunqClient(context)` instance.

### Manual Refresh

`Context.refreshSession()` creates a new session with the same device and installation and returns a new `Context`. An existing client does not pick it up; create a new client from the returned context:

```kotlin
val refreshedContext = context.refreshSession()
val refreshedClient = bunqClient(refreshedContext)
```

### Session Expiry Time

Every `Context` contains the session expiry time:

```kotlin
import java.time.Instant

val expiryTime: Instant = context.sessionExpiryTime
val willExpireSoon = expiryTime.isBefore(Instant.now().plusSeconds(5 * 60))
```

## Persist and restore a Context

`initContext` registers an installation and a device, which you only need once per API key. Store the `Context` and build the client from it on the next start instead of calling `initContext` again.

Store every field of `Context`: `serverPublicKey`, `deviceId`, `sessionId`, `sessionToken`, `userId`, `sessionExpiryTime`, `installationToken` and the secrets in `config` (API key and signing keys). The SDK has no serialisation format of its own. Treat the stored data as a secret and store it encrypted (`toString()` masks secrets in log output only; the object still holds them).

Pass `onContextChange` to `bunqClient` to receive the new `Context` after every refresh, whether triggered by a 403 or by expiry. It is called once per refresh. If it throws, the exception reaches the caller of the request that triggered the refresh.

```kotlin
// first start
val context = initContext(config)
save(context)

// later starts: build the Context from the stored fields (config is supplied again by your code)
val restored = Context(
    serverPublicKey = stored.serverPublicKey,
    deviceId = stored.deviceId,
    sessionId = stored.sessionId,
    sessionToken = stored.sessionToken,
    userId = stored.userId,
    sessionExpiryTime = stored.sessionExpiryTime,
    installationToken = stored.installationToken,
    config = config,
)
val client = bunqClient(restored, onContextChange = { save(it) })
```

If `sessionExpiryTime` is in the past or less than 30 seconds away, the client refreshes the session before the first request, so a stored context that expired while the app was stopped works. Concurrent calls share one refresh. If that refresh fails, the request is sent with the old token; if bunq answers 403 "Insufficient authentication.", that 403 is returned as the error without a second refresh. If bunq no longer accepts the stored installation or device, the refresh fails; call `initContext` again.

## Logging

The SDK logs through [kotlin-logging](https://github.com/oshai/kotlin-logging) on top of `slf4j-api`. It ships no logging backend; add one (for example Logback or `slf4j-simple`) to see the output. Spring Boot apps already have a backend through `spring-boot-starter-logging` (Logback), so they need nothing extra. The method, URI and status of each request are logged at debug level, and a failed session refresh is logged as a warning. Credentials are never logged. `Context.toString()` and `Config.toString()` mask secrets; the object still holds them, so store it encrypted.

## Response Signatures

bunq signs every response: the `X-Bunq-Server-Signature` header holds a base64 SHA256withRSA (PKCS#1 v1.5) signature over the raw response body bytes. Every 200 and 400 response that reaches the generated client is verified against `Context.serverPublicKey`, the server public key bunq returned when the installation was created. The requests of `initContext` after the installation are verified with that key as well.

A response without the header, or with a signature that does not match the body, is rejected with `SecurityException("Invalid bunq server signature")`; the exception is thrown from the call. Other statuses (403, 404, 5xx, ...) are thrown as the API error described under Error Handling before the signature is looked at.

The installation response itself is not verified: the key it carries is not known yet, so it only proves that the sender holds the key it announces. The pinned certificate of the `BunqServer` is what protects that call.

## Error Handling

See [Error Handling in the README](../README.md#error-handling) for when the exception is thrown.

A 400 is returned as `Response400`, whose body has `Error[]` with an `error_description` per entry. Every other outcome throws `BunqApiException(status, body)` (unchecked, in `com.bunq.sdk`); `body` is the full response body as a string and the message is `bunq answered <status>: <first 500 characters>`. A `when` over `Response200` and `Response400` is exhaustive:

```kotlin
import com.bunq.sdk.BunqApiException

suspend fun readUserOrNull(context: Context, userId: Long): UserRead? {
    val client = bunqClient(context)
    return try {
        when (val res = client.readUser(userId)) {
            is ReadUser.Response200 -> res.body
            is ReadUser.Response400 -> error("bunq answered 400: ${res.body.Error?.map { it.error_description }}")
        }
    } catch (e: BunqApiException) {
        if (e.status == 404) null else throw e
    }
}
```

`initContext` and `Context.refreshSession()` throw if:

- bunq answers a setup request with a typed 400: `IllegalStateException("Cannot create session server (status 400): <error_description>")` (the step is "create installation", "create device server" or "create session server")
- bunq answers with any other status: `BunqApiException`
- required session information is missing from the API response (`IllegalStateException`)

```kotlin
try {
    val refreshedContext = context.refreshSession()
} catch (e: Exception) {
    println("Session refresh failed: ${e.message}")
}
```
