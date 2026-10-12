# Java SDK - Session Management

## Overview

The bunq Java SDK provides session management through the `Context` class. Sessions automatically expire and need to be refreshed periodically to maintain API access.

## Session Expiry

### Check Session Expiry Time

```java
import java.time.Instant;

Context context = Context.initContext(config);
Instant expiryTime = context.sessionExpiryTime();

// Check if session will expire soon
boolean willExpireSoon = expiryTime.isBefore(Instant.now().plusSeconds(5 * 60)); // 5 minutes
```

## Session Refresh

### Refresh an Existing Session

Use the `refreshSession()` instance method. It creates a new session with the same device and installation and returns a new `Context`:

```java
Context refreshedContext = context.refreshSession();
```

### Complete Example

```java
import com.bunq.sdk.BunqSigningKeysGenerator;
import com.bunq.sdk.BunqServer;
import com.bunq.sdk.Config;
import com.bunq.sdk.Context;
import java.time.Instant;

Config config = new Config(
    BunqServer.BUNQ_SANDBOX_SERVER,
    "MyApp",
    "your-api-key",
    BunqSigningKeysGenerator.generateBunqSigningKeys(),
    null, null, null, null, null, null
);

Context context = Context.initContext(config);

// Later, refresh when the session is about to expire
if (context.sessionExpiryTime().isBefore(Instant.now().plusSeconds(5 * 60))) {
    context = context.refreshSession();
}
```

## Context Properties

The `Context` class includes the following session-related properties:

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

When working with sessions, handle potential errors:

```java
try {
    Context context = Context.initContext(config);
    // Use context for API calls
} catch (Exception error) {
    System.err.println("Session creation failed: " + error.getMessage());
    // Handle error appropriately
}
```

## Best Practices

1. **Implement retry logic**: When API calls fail due to expired sessions, refresh the context and retry
2. **Store contexts securely**: Session tokens should be stored securely if persistence is needed
3. **Monitor for session errors**: Watch for authentication-related exceptions

```java
import java.util.concurrent.CompletableFuture;
import java.util.function.Function;

public static <T> CompletableFuture<T> apiCallWithSessionRetry(
    Function<Context, CompletableFuture<T>> apiCallFunction,
    Context context,
    Config config,
    int maxRetries
) {
    /**
     * Execute an API call with automatic session refresh on failure.
     */
    return apiCallFunction.apply(context)
        .handle((result, throwable) -> {
            if (throwable != null) {
                String errorMessage = throwable.getMessage().toLowerCase();
                if (maxRetries > 0 && (errorMessage.contains("session") || errorMessage.contains("unauthorized"))) {
                    System.out.println("Session error, refreshing context and retrying...");
                    Context newContext = context.refreshSession();
                    return apiCallWithSessionRetry(apiCallFunction, newContext, config, maxRetries - 1);
                } else {
                    return CompletableFuture.<T>failedFuture(throwable);
                }
            } else {
                return CompletableFuture.completedFuture(result);
            }
        })
        .thenCompose(Function.identity());
}

// Usage example
Function<Context, CompletableFuture<String>> getUserInfo = (context) -> {
    // Implementation would make actual API call using context
    return CompletableFuture.completedFuture("user info");
};

CompletableFuture<String> result = apiCallWithSessionRetry(
    getUserInfo,
    context,
    config,
    1 // max retries
);
```

## Immutability

The `Context` class is immutable, which means:

1. **Thread-safe**: Can be safely shared across multiple threads
2. **Predictable**: State cannot change after creation
3. **Session refresh returns new instance**: `refreshSession()` returns a new `Context` instance

```java
// Context is immutable - this is safe
Context sharedContext = Context.initContext(config);

Context refreshedContext = sharedContext.refreshSession();
// sharedContext remains unchanged, refreshedContext is a new instance
```
