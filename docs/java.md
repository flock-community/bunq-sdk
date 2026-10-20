# Java SDK

## Requirements

- Java 17+ (the package is built with a Java 17 toolchain)
- Jackson 2 (included as a dependency)

## Install

Add the JitPack repository and depend on a release tag. The published artifacts of 0.0.3 and earlier have the old `Sdk`/`handler` API; the client described here ships from 0.1.0.

Gradle (Kotlin DSL):

```kotlin
repositories {
    maven("https://jitpack.io")
    mavenCentral()
}

dependencies {
    implementation("com.github.flock-community.bunq-sdk:java:0.1.0")
}
```

Maven:

```xml
<repositories>
  <repository>
    <id>jitpack.io</id>
    <url>https://jitpack.io</url>
  </repository>
</repositories>

<dependency>
  <groupId>com.github.flock-community.bunq-sdk</groupId>
  <artifactId>java</artifactId>
  <version>&lt;release&gt;</version>
</dependency>
```

To build from source instead, publish the package to your local Maven repository, add `mavenLocal()` to `repositories` and depend on `com.github.flock-community.bunq-sdk:java:0.0.1-SNAPSHOT`:

```bash
./gradlew :packages:java:publishToMavenLocal
```

## Creating a Context

```java
import com.bunq.sdk.BunqServer;
import com.bunq.sdk.BunqSigningKeysGenerator;
import com.bunq.sdk.Config;
import com.bunq.sdk.Context;

Config config = new Config(
    BunqServer.BUNQ_SANDBOX_SERVER,
    "MyApp",
    "your-api-key",
    BunqSigningKeysGenerator.generateBunqSigningKeys(),
    null, null, null, null, null, null // userAgent, cacheControl, language, region, clientRequestId, geolocation
);

Context context = Context.initContext(config);
```

`generateBunqSigningKeys()` creates a new key pair on every call. To keep the same keys across restarts, use `generateBunqSigningKeys(privateKeyFile, publicKeyFile)`, or use the constructor `new Config(server, serviceName, apiKey, privateKeyPem, publicKeyPem)` with stored PEM strings.

## Creating the Client and Calling an Endpoint

`Wirespec.bunqClient(context)` returns the client that Wirespec generates. Its methods return a `CompletableFuture` and are named after the operation id in camelCase (`readUser`, `listAllMonetaryAccountBankForUser`). Optional query parameters are `Optional` values: pass `Optional.empty()` for the ones you do not use.

```java
import com.bunq.sdk.Wirespec;
import com.bunq.sdk.generated.Client;
import com.bunq.sdk.generated.endpoint.ListAllMonetaryAccountBankForUser;
import com.bunq.sdk.generated.endpoint.ReadUser;
import com.bunq.sdk.generated.model.ErrorArray;
import com.bunq.sdk.generated.model.UserPerson;
import java.util.Optional;

Client client = Wirespec.bunqClient(context);

ReadUser.Response<?> user = client.readUser(context.userId()).get();
if (user instanceof ReadUser.Response200 response) {
    String legalName = response.body().UserPerson().flatMap(UserPerson::legal_name).orElse(null);
} else if (user instanceof ReadUser.Response400 error) {
    System.err.println(error.body().Error());
}

ListAllMonetaryAccountBankForUser.Response<?> accounts = client
    .listAllMonetaryAccountBankForUser(context.userId(), Optional.empty(), Optional.empty(), Optional.empty())
    .get();
if (accounts instanceof ListAllMonetaryAccountBankForUser.Response200 response) {
    response.body().forEach(account -> System.out.println(account.display_name().orElse("")));
} else if (accounts instanceof ListAllMonetaryAccountBankForUser.Response400 error) {
    System.err.println(error.body().Error());
}
```

## Session Refresh

See [Session Refresh in the README](../README.md#session-refresh) for how the client refreshes the session, what happens when the refresh fails (the call throws `BunqApiException` with status 403), and the manual refresh.

The shared refresh is guarded by a `ReentrantLock`, and the refresh-failure warning is logged through `System.Logger`. Keep using the same `Wirespec.bunqClient(context)` instance.

### Manual Refresh

`context.refreshSession()` creates a new session with the same device and installation and returns a new `Context`. An existing client does not pick it up; create a new client from the returned context:

```java
Context refreshedContext = context.refreshSession();
Client refreshedClient = Wirespec.bunqClient(refreshedContext);
```

### Session Expiry Time

```java
import java.time.Instant;

Instant expiryTime = context.sessionExpiryTime();
boolean willExpireSoon = expiryTime.isBefore(Instant.now().plusSeconds(5 * 60));
```

## Context Properties

`Context` is an immutable record, so it can be shared between threads. `refreshSession()` returns a new instance and leaves the original unchanged.

```java
public record Context(
    String serverPublicKey,
    long deviceId,
    long sessionId,
    String sessionToken,
    long userId,
    Instant sessionExpiryTime,
    String installationToken,
    Config config
) {}
```

## Error Handling

See [Error Handling in the README](../README.md#error-handling) for when the exception is thrown.

A 400 is returned as `Response400`, whose body has `Error[]` with an `error_description` per entry. Every other outcome throws `BunqApiException` (unchecked, in `com.bunq.sdk`) with `status()` and `body()`, the full response body as a string; the message is `bunq answered <status>: <first 500 characters>`. The exception arrives wrapped, in a `CompletionException` from `join()` and in an `ExecutionException` from `get()`, so check `getCause()`:

```java
import com.bunq.sdk.BunqApiException;
import java.util.concurrent.CompletionException;

try {
    ReadUser.Response<?> user = client.readUser(999999999L).join();
    if (user instanceof ReadUser.Response400 error) {
        String description = error.body().Error().flatMap(errors -> errors.stream().findFirst()).flatMap(ErrorArray::error_description).orElse(null);
        throw new IllegalStateException("bunq answered 400: " + description);
    }
} catch (CompletionException e) {
    if (e.getCause() instanceof BunqApiException api && api.status() == 404) {
        System.out.println("No such user");
    } else {
        throw e;
    }
}
```

`Context.initContext` and `refreshSession()` throw an exception if session creation fails. A typed 400 gives the message `Cannot create session server (status 400): <error_description>` (the step is "create installation", "create device server" or "create session server"); any other status gives a `BunqApiException`. `initContext` wraps either in a `RuntimeException` whose message is the cause's `toString()` (cause chain: `ExecutionException`, then the `RuntimeException` or `BunqApiException`). `refreshSession()` wraps it in `RuntimeException("Failed to refresh session")` with the same cause chain:

```java
try {
    Context context = Context.initContext(config);
} catch (Exception error) {
    System.err.println("Session creation failed: " + error.getMessage());
}
```
