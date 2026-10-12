# Kotlin SDK

## Requirements

- Kotlin 2.3+ and JVM 17+
- Wirespec 0.21.x runtime (a consumer that uses Wirespec itself must use 0.21.x as well, because both share one runtime on the classpath)
- kotlinx-coroutines in your own project: the client functions are `suspend`

## Install

There is no versioned release yet. Publish the package to your local Maven repository and depend on it:

```bash
./gradlew :packages:kotlin:publishToMavenLocal
```

```kotlin
repositories {
    mavenLocal()
    mavenCentral()
}

dependencies {
    implementation("com.github.flock-community.bunq-sdk:kotlin:0.0.1-SNAPSHOT")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.10.1")
}
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

`bunqClient(context)` returns the client that Wirespec generates. Its methods are `suspend` functions named after the operation id in camelCase (`readUser`, `listAllMonetaryAccountBankForUser`). Query parameters have no defaults: pass `null` for the ones you do not use.

```kotlin
import com.bunq.sdk.bunqClient
import com.bunq.sdk.generated.endpoint.ListAllMonetaryAccountBankForUser
import com.bunq.sdk.generated.endpoint.ReadUser

suspend fun readLegalName(context: Context): String? {
    val client = bunqClient(context)
    return when (val res = client.readUser(context.userId)) {
        is ReadUser.Response200 -> res.body.UserPerson?.legal_name
        is ReadUser.Response400 -> error("Cannot read user")
    }
}

suspend fun listAccountNames(context: Context): List<String?> {
    val client = bunqClient(context)
    return when (val res = client.listAllMonetaryAccountBankForUser(context.userId, null, null, null)) {
        is ListAllMonetaryAccountBankForUser.Response200 -> res.body.map { it.display_name }
        else -> error("Cannot list monetary accounts")
    }
}
```

## Session Refresh

The client refreshes the session for you. When bunq answers with 403 "Insufficient authentication." (the response for an expired or deleted session), the client:

1. creates a new session once and retries the request with the new token, signed again;
2. shares that one refresh between concurrent calls (guarded by a `Mutex`), and uses the new token for later calls on the same client.

If the refresh fails, the original 403 response is returned and a warning is logged. Other 403 responses are returned unchanged.

Keep using the same `bunqClient(context)` instance so that calls share the refreshed session.

### Manual Refresh

`Context.refreshSession()` is still available. It creates a new session with the same device and installation and returns a new `Context`:

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

The SDK logs through [kotlin-logging](https://github.com/oshai/kotlin-logging) on top of `slf4j-api`. It ships no logging backend; add one (for example Logback or `slf4j-simple`) to see the output. Spring Boot apps already have a backend through `spring-boot-starter-logging` (Logback), so they need nothing extra. The method, URI and status of each request are logged at debug level, and credentials are never logged.

## Error Handling

`initContext` and `Context.refreshSession()` throw an exception if:

- the bunq API returns an error during session creation
- required session information is missing from the API response

```kotlin
try {
    val refreshedContext = context.refreshSession()
} catch (e: Exception) {
    println("Session refresh failed: ${e.message}")
}
```
