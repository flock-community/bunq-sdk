# Kotlin SDK - Session Management

## Overview

The bunq Kotlin SDK provides simple session management through the `Context` data class and extension functions. Sessions automatically expire and need to be refreshed periodically to maintain API access.

## Session Expiry

### Check Session Expiry Time

Every `Context` instance contains the session expiry time:

```kotlin
val context = initContext(config, signing)
val expiryTime: Instant? = context.sessionExpiryTime

// Check if session will expire soon
val willExpireSoon = expiryTime?.let { 
    it.isBefore(Instant.now().plusMinutes(5))
} ?: true
```

## Session Refresh

### Refresh an Existing Session

Use the `refreshSession()` extension function to refresh your session:

```kotlin
val config = Config(
    bunqServer = BUNQ_SANDBOX_SERVER,
    serviceName = "MyApp",
    apiKey = "your-api-key",
    // ... other config
)

// Refresh the session
val refreshedContext = context.refreshSession(config)

// Use the new context for subsequent API calls
```

### Complete Example

```kotlin
fun maintainSession(initialContext: Context, config: Config): Context {
    val expiryTime = initialContext.sessionExpiryTime
    
    return if (expiryTime != null && expiryTime.isBefore(Instant.now().plusMinutes(5))) {
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
- The same `Config` used for initial context creation should be used for refresh
- A new `Context` instance is returned with updated session information

## Error Handling

The `refreshSession()` function will throw an error if:
- No installation token is available in the context
- The bunq API returns an error during session creation
- Required session information is missing from the API response

```kotlin
try {
    val refreshedContext = context.refreshSession(config)
    // Use refreshed context
} catch (e: Exception) {
    println("Session refresh failed: ${e.message}")
    // Handle error or re-initialize context
}
```