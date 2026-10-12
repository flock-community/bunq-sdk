# Kotlin SDK - Session Management

## Overview

The bunq Kotlin SDK provides simple session management through the `Context` data class and extension functions. Sessions automatically expire and need to be refreshed periodically to maintain API access.

## Session Expiry

### Check Session Expiry Time

Every `Context` instance contains the session expiry time:

```kotlin
val context = initContext(config)
val expiryTime: Instant = context.sessionExpiryTime

// Check if session will expire soon
val willExpireSoon = expiryTime.isBefore(Instant.now().plusSeconds(5 * 60))
```

## Session Refresh

### Refresh an Existing Session

Use the `refreshSession()` extension function to refresh your session:

```kotlin
val config = Config(
    bunqServer = BUNQ_SANDBOX_SERVER,
    serviceName = "MyApp",
    apiKey = "your-api-key",
    signingKeys = BunqSigningKeysGenerator.generateBunqSigningKeys(),
)

// Refresh the session
val refreshedContext = context.refreshSession()

// Use the new context for subsequent API calls
```

### Complete Example

```kotlin
fun maintainSession(initialContext: Context): Context {
    val expiryTime = initialContext.sessionExpiryTime
    
    return if (expiryTime.isBefore(Instant.now().plusSeconds(5 * 60))) {
        // Session expires in less than 5 minutes, refresh it
        println("Session expiring soon, refreshing...")
        initialContext.refreshSession(config)
    } else {
        // Session is still valid
        initialContext
    }
}
```

## Requirements

- The context must contain a valid `installationToken` to refresh sessions
- The refresh uses the `Config` stored in the context
- A new `Context` instance is returned with updated session information

## Logging

The SDK logs through [kotlin-logging](https://github.com/oshai/kotlin-logging) on top of `slf4j-api`. It ships no logging backend; add one (for example Logback or `slf4j-simple`) to see the output. Request and response details are logged at debug level, and credentials are never logged.

## Error Handling

The `refreshSession()` function will throw an error if:
- No installation token is available in the context
- The bunq API returns an error during session creation
- Required session information is missing from the API response

```kotlin
try {
    val refreshedContext = context.refreshSession()
    // Use refreshed context
} catch (e: Exception) {
    println("Session refresh failed: ${e.message}")
    // Handle error or re-initialize context
}
```