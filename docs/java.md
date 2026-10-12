# Java SDK

## Requirements

- Java 17+ (the package is built with a Java 17 toolchain)
- Jackson 2 (included as a dependency)

## Install

There is no versioned release yet. Publish the package to your local Maven repository and depend on it:

```bash
./gradlew :packages:java:publishToMavenLocal
```

```kotlin
repositories {
    mavenLocal()
    mavenCentral()
}

dependencies {
    implementation("com.github.flock-community.bunq-sdk:java:0.0.1-SNAPSHOT")
}
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
import com.bunq.sdk.generated.model.UserPerson;
import java.util.Optional;

Client client = Wirespec.bunqClient(context);

ReadUser.Response<?> user = client.readUser(context.userId()).get();
if (user instanceof ReadUser.Response200 response) {
    String legalName = response.body().UserPerson().flatMap(UserPerson::legal_name).orElse(null);
}

ListAllMonetaryAccountBankForUser.Response<?> accounts = client
    .listAllMonetaryAccountBankForUser(context.userId(), Optional.empty(), Optional.empty(), Optional.empty())
    .get();
if (accounts instanceof ListAllMonetaryAccountBankForUser.Response200 response) {
    response.body().forEach(account -> System.out.println(account.display_name().orElse("")));
}
```

## Session Refresh

See [Session Refresh in the README](../README.md#session-refresh) for how the client refreshes the session, what happens when the refresh fails, and the manual refresh.

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

`Context.initContext` and `refreshSession()` throw an exception if session creation fails:

```java
try {
    Context context = Context.initContext(config);
} catch (Exception error) {
    System.err.println("Session creation failed: " + error.getMessage());
}
```
