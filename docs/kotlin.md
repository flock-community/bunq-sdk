# Kotlin SDK

## Requirements

- Kotlin 2.3+ and JVM 17+
- Wirespec 0.21.x runtime (a consumer that uses Wirespec itself must use 0.21.x as well, because both share one runtime on the classpath)
- kotlinx-coroutines in your own project: the client functions are `suspend`

## Install

Add the JitPack repository and depend on a release tag. The published artifacts of 0.0.3 and earlier have the old `Sdk`/`handler` API; the client described here ships in the first release after #8. Replace `<release>` with that tag.

```kotlin
repositories {
    maven("https://jitpack.io")
    mavenCentral()
}

dependencies {
    implementation("com.github.flock-community.bunq-sdk:kotlin:<release>")
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

`Context.toString()` and `Config.toString()` mask secrets; the object still holds them, so store it encrypted.

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

## Logging

The SDK logs through [kotlin-logging](https://github.com/oshai/kotlin-logging) on top of `slf4j-api`. It ships no logging backend; add one (for example Logback or `slf4j-simple`) to see the output. Spring Boot apps already have a backend through `spring-boot-starter-logging` (Logback), so they need nothing extra. The method, URI and status of each request are logged at debug level, and a failed session refresh is logged as a warning. Credentials are never logged.

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
