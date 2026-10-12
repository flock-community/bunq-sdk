# TypeScript/npm SDK - Session Management

## Overview

The bunq TypeScript SDK provides session management through the `Context` type and related functions. Sessions automatically expire and need to be refreshed periodically to maintain API access.

## Session Expiry

### Check Session Expiry Time

Every `Context` instance contains the session expiry information:

```typescript
const context = await initContext(config);
const expiryTime: Date = context.sessionExpiryTime;

// Check if session will expire soon
const willExpireSoon = expiryTime.getTime() < Date.now() + (5 * 60 * 1000); // 5 minutes
```

## Session Refresh

### Refresh an Existing Session

Use `refreshSession(context)`. It creates a new session with the same device and installation and returns a new `Context`:

```typescript
import {refreshSession} from "./context";

const refreshedContext = await refreshSession(context);
```

### Complete Example

```typescript
async function maintainSession(currentContext: Context): Promise<Context> {
  const expiryTime = currentContext.sessionExpiryTime;

  if (expiryTime.getTime() < Date.now() + (5 * 60 * 1000)) {
    // Session expires in less than 5 minutes, refresh it
    console.log('Session expiring soon, refreshing...');
    return await refreshSession(currentContext);
  } else {
    // Session is still valid
    return currentContext;
  }
}
```

## Context Properties

The `Context` type includes the following session-related properties:

```typescript
interface Context {
  readonly serverPublicKey: string;
  readonly deviceId: number;
  readonly sessionId: number;
  readonly sessionToken: string;
  readonly userId: number;
  readonly sessionExpiryTime: Date;
  readonly installationToken: string;
  readonly config: Config;
}
```

## Error Handling

When working with sessions, handle potential errors:

```typescript
try {
  const context = await initContext(config);
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
  context: Context
): Promise<{ result: T; context: Context }> {
  let currentContext = context;
  
  // Check if session needs refresh
  if (currentContext.sessionExpiryTime.getTime() < Date.now() + (5 * 60 * 1000)) {
    currentContext = await refreshSession(currentContext);
  }
  
  try {
    const result = await apiCall(currentContext);
    return { result, context: currentContext };
  } catch (error) {
    // If API call fails, try refreshing session once
    currentContext = await refreshSession(currentContext);
    const result = await apiCall(currentContext);
    return { result, context: currentContext };
  }
}
```