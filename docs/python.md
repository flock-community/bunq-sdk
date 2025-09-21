# Python SDK - Session Management

## Overview

The bunq Python SDK provides session management through the `Context` class. Sessions automatically expire and need to be refreshed periodically to maintain API access.

## Session Expiry

### Check Session Expiry Time

> **Note**: Session expiry time tracking is planned for future implementation. Currently, the Python SDK doesn't expose session expiry information directly.

**Planned API:**

```python
from datetime import datetime, timedelta
from context import Context
from config import Config

context = Context(config)

# This will be available in a future version
expiry_time = context.session_expiry_time  # datetime object

# Check if session will expire soon
will_expire_soon = expiry_time and expiry_time < datetime.now() + timedelta(minutes=5)
```

## Session Refresh

### Refresh an Existing Session

> **Note**: Session refresh functionality is planned for future implementation. Currently, you need to create a new context when sessions expire.

**Planned API:**

```python
def refresh_session(context: Context) -> Context:
    """Refresh the session for an existing context."""
    # Implementation planned
    pass
```

### Current Workaround

For now, when a session expires, create a new context:

```python
from context import Context
from config import Config

def maintain_session(current_context: Context, config: Config) -> Context:
    """
    Maintain session by creating a new context when needed.
    This is a workaround until refresh functionality is implemented.
    """
    try:
        # Try to use current context for an API call to test validity
        # If it fails, create a new context
        return current_context
    except Exception as e:
        if "session" in str(e).lower() or "unauthorized" in str(e).lower():
            print("Session expired, creating new context...")
            return Context(config)
        else:
            raise e

# Usage
config = Config(
    api_key="your-api-key",
    service_name="MyApp",
    # ... other config
)

context = Context(config)

# Later, when you suspect session might be expired
context = maintain_session(context, config)
```

## Context Properties

The `Context` class includes the following session-related properties:

```python
class Context:
    def __init__(self, config: Config):
        self.config = config
        self.api_key = config.api_key
        self.service_name = config.service_name
        self.server_public_key = "..."  # From installation
        self.device_id = 123             # From device server creation
        self.session_id = 456            # From session server creation  
        self.session_token = "..."       # Session authentication token
        self.user_id = 789              # User ID from session
        # session_expiry_time - planned for future implementation
```

## Error Handling

When working with sessions, handle potential errors:

```python
try:
    context = Context(config)
    # Use context for API calls
except Exception as error:
    print(f"Session creation failed: {error}")
    # Handle error appropriately
```

## Best Practices

1. **Implement retry logic**: When API calls fail due to expired sessions, create new context and retry
2. **Store contexts securely**: Session tokens should be stored securely if persistence is needed
3. **Monitor for session errors**: Watch for authentication-related exceptions

```python
import time
from typing import Optional

def api_call_with_session_retry(
    api_call_func,
    context: Context, 
    config: Config,
    max_retries: int = 1
) -> tuple:
    """
    Execute an API call with automatic session refresh on failure.
    Returns tuple of (result, updated_context).
    """
    current_context = context
    last_exception = None
    
    for attempt in range(max_retries + 1):
        try:
            result = api_call_func(current_context)
            return result, current_context
        except Exception as e:
            last_exception = e
            if attempt < max_retries and ("session" in str(e).lower() or "unauthorized" in str(e).lower()):
                print(f"Session error on attempt {attempt + 1}, creating new context...")
                current_context = Context(config)
                time.sleep(1)  # Brief delay before retry
            else:
                break
    
    raise last_exception

# Usage example
def get_user_info(context: Context):
    """Example API call function."""
    # Implementation would make actual API call using context
    pass

result, updated_context = api_call_with_session_retry(
    get_user_info, 
    context, 
    config
)
```

## Future Enhancements

The Python SDK will be enhanced with:

1. **Session expiry tracking**: Automatic tracking of when sessions expire
2. **Refresh functionality**: Ability to refresh sessions without full context recreation
3. **Automatic session management**: Built-in handling of session expiry and refresh
4. **Session persistence**: Options to save and restore session state