# TypeScript/npm SDK - Session Management

## Overview

The bunq TypeScript SDK provides session management through the `Context` type and related functions. Sessions automatically expire and need to be refreshed periodically to maintain API access.

## Session Expiry

### Check Session Expiry Time

Every `Context` instance contains the session expiry information:

```typescript
const context = await initContext(config, signing);
const expiryTime: Date | undefined = context.sessionExpiryTime;

// Check if session will expire soon
const willExpireSoon = expiryTime 
  ? expiryTime.getTime() < Date.now() + (5 * 60 * 1000) // 5 minutes
  : true;
```

## Session Refresh

### Refresh an Existing Session

> **Note**: Session refresh functionality is planned for future implementation. Currently, you need to create a new context when sessions expire.

**Planned API:**

```typescript
// This will be available in a future version
export async function refreshSession(
  context: Context, 
  config: Config, 
  signing: Signing
): Promise<Context> {
  // Implementation planned
}
```

### Current Workaround

For now, when a session expires, create a new context:

```typescript
async function maintainSession(
  currentContext: Context, 
  config: Config, 
  signing: Signing
): Promise<Context> {
  const expiryTime = currentContext.sessionExpiryTime;
  
  if (expiryTime && expiryTime.getTime() < Date.now() + (5 * 60 * 1000)) {
    // Session expires in less than 5 minutes, create new context
    console.log('Session expiring soon, creating new context...');
    return await initContext(config, signing);
  } else {
    // Session is still valid
    return currentContext;
  }
}
```

## Context Properties

The `Context` type includes the following session-related properties:

```typescript
type Context = {
  apiKey: string;
  serverName: string;
  serverPublicKey: string;
  deviceId: number;
  sessionId: number;
  sessionToken: string;
  userId: number;
  sessionExpiryTime?: Date;        // When the session expires
  sessionTimeoutSeconds?: number;  // Session duration in seconds
  // ... other properties
}
```

## Error Handling

When working with sessions, handle potential errors:

```typescript
try {
  const context = await initContext(config, signing);
  // Use context for API calls
} catch (error) {
  console.error('Session creation failed:', error.message);
  // Handle error appropriately
}
```

## Best Practices

1. **Check expiry before API calls**: Always verify session validity before making API requests
2. **Implement retry logic**: When API calls fail due to expired sessions, refresh and retry
3. **Store contexts securely**: Session tokens should be stored securely if persistence is needed

```typescript
async function apiCallWithSessionCheck<T>(
  apiCall: (context: Context) => Promise<T>,
  context: Context,
  config: Config,
  signing: Signing
): Promise<{ result: T; context: Context }> {
  let currentContext = context;
  
  // Check if session needs refresh
  if (currentContext.sessionExpiryTime && 
      currentContext.sessionExpiryTime.getTime() < Date.now() + (5 * 60 * 1000)) {
    currentContext = await initContext(config, signing);
  }
  
  try {
    const result = await apiCall(currentContext);
    return { result, context: currentContext };
  } catch (error) {
    // If API call fails, try refreshing session once
    currentContext = await initContext(config, signing);
    const result = await apiCall(currentContext);
    return { result, context: currentContext };
  }
}
```