# Java SDK - Session Management

## Overview

The bunq Java SDK provides session management through the `Context` class. Sessions automatically expire and need to be refreshed periodically to maintain API access.

## Session Expiry

### Check Session Expiry Time

> **Note**: Session expiry time tracking is planned for future implementation. Currently, the Java SDK doesn't expose session expiry information directly.

**Planned API:**

```java
import java.time.Instant;

Context context = Context.initContext(config);

// This will be available in a future version
Instant expiryTime = context.getSessionExpiryTime(); // Optional<Instant>

// Check if session will expire soon
boolean willExpireSoon = expiryTime != null && 
    expiryTime.isBefore(Instant.now().plusSeconds(5 * 60)); // 5 minutes
```

## Session Refresh

### Refresh an Existing Session

> **Note**: Session refresh functionality is planned for future implementation. Currently, you need to create a new context when sessions expire.

**Planned API:**

```java
public static Context refreshSession(Context context, Config config) {
    // Implementation planned
    return null;
}
```

### Current Workaround

For now, when a session expires, create a new context:

```java
import com.bunq.sdk.Context;
import com.bunq.sdk.Config;

public static Context maintainSession(Context currentContext, Config config) {
    /*
     * Maintain session by creating a new context when needed.
     * This is a workaround until refresh functionality is implemented.
     */
    try {
        // Try to use current context for an API call to test validity
        // If it succeeds, return current context
        return currentContext;
    } catch (Exception e) {
        String errorMessage = e.getMessage().toLowerCase();
        if (errorMessage.contains("session") || errorMessage.contains("unauthorized")) {
            System.out.println("Session expired, creating new context...");
            return Context.initContext(config);
        } else {
            throw new RuntimeException("Unexpected error", e);
        }
    }
}

// Usage
Config config = new Config(
    "your-api-key",
    "MyApp"
    // ... other config parameters
);

Context context = Context.initContext(config);

// Later, when you suspect session might be expired
context = maintainSession(context, config);
```

## Context Properties

The `Context` class includes the following session-related properties:

```java
public class Context {
    private final String apiKey;
    private final String serviceName; 
    private final String serverPublicKey;
    private final long deviceId;
    private final long sessionId;        // Session identifier
    private final String sessionToken;  // Session authentication token
    private final long userId;          // User ID from session
    
    // Getters available:
    public String getApiKey() { return apiKey; }
    public String getServiceName() { return serviceName; }
    public String getServerPublicKey() { return serverPublicKey; }
    public long getDeviceId() { return deviceId; }
    public long getSessionId() { return sessionId; }
    public String getSessionToken() { return sessionToken; }
    public long getUserId() { return userId; }
    
    // Planned for future implementation:
    // public Optional<Instant> getSessionExpiryTime() { ... }
}
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

1. **Implement retry logic**: When API calls fail due to expired sessions, create new context and retry
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
                    System.out.println("Session error, creating new context and retrying...");
                    Context newContext = Context.initContext(config);
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
3. **Session refresh returns new instance**: When refresh is implemented, it will return a new `Context` instance

```java
// Context is immutable - this is safe
Context sharedContext = Context.initContext(config);

// When refresh is implemented, it will work like this:
Context refreshedContext = Context.refreshSession(sharedContext, config);
// sharedContext remains unchanged, refreshedContext is a new instance
```

## Future Enhancements

The Java SDK will be enhanced with:

1. **Session expiry tracking**: `Optional<Instant> getSessionExpiryTime()` method
2. **Refresh functionality**: `static Context refreshSession(Context context, Config config)` method
3. **Automatic session management**: Built-in handling of session expiry and refresh
4. **Builder pattern**: Fluent API for context creation with optional parameters