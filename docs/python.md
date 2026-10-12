# Python SDK - Session Management

## Overview

The bunq Python SDK provides session management through the `Context` class. Sessions automatically expire and need to be refreshed periodically to maintain API access.

## Session Expiry

### Check Session Expiry Time

```python
from datetime import datetime, timedelta
from context import Context, init_context
from config import Config

context = init_context(config)
expiry_time = context.session_expiry_time  # datetime object

# Check if session will expire soon
will_expire_soon = expiry_time < datetime.now() + timedelta(minutes=5)
```

## Session Refresh

### Refresh an Existing Session

Use `refresh_session(context)`. It creates a new session with the same device and installation and returns a new `Context`:

```python
from context import refresh_session

refreshed_context = refresh_session(context)
```

### Complete Example

```python
from datetime import datetime, timedelta
from context import Context, init_context, refresh_session
from config import create_config
from bunq_server import BUNQ_SANDBOX_SERVER
from bunq_signing_keys_generator import BunqSigningKeysGenerator

private_key_pem, public_key_pem = BunqSigningKeysGenerator.generate_bunq_signing_keys_as_pem()
config = create_config(
    bunq_server=BUNQ_SANDBOX_SERVER,
    service_name="MyApp",
    api_key="your-api-key",
    private_key_pem=private_key_pem,
    public_key_pem=public_key_pem,
)

context = init_context(config)

# Later, refresh when the session is about to expire
if context.session_expiry_time < datetime.now() + timedelta(minutes=5):
    context = refresh_session(context)
```

## Context Properties

The `Context` class includes the following session-related properties:

```python
@dataclass
class Context:
    server_public_key: str
    device_id: int
    session_id: int
    session_token: str
    user_id: int
    session_expiry_time: datetime
    installation_token: str
    config: Config
```

## Error Handling

When working with sessions, handle potential errors:

```python
try:
    context = init_context(config)
    # Use context for API calls
except Exception as error:
    print(f"Session creation failed: {error}")
    # Handle error appropriately
```

## Best Practices

1. **Implement retry logic**: When API calls fail due to expired sessions, refresh the context and retry
2. **Store contexts securely**: Session tokens should be stored securely if persistence is needed
3. **Monitor for session errors**: Watch for authentication-related exceptions

```python
import time
from context import Context, refresh_session
from config import Config
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
    last_exception: Exception | None = None
    
    for attempt in range(max_retries + 1):
        try:
            result = api_call_func(current_context)
            return result, current_context
        except Exception as e:
            last_exception = e
            if attempt < max_retries and ("session" in str(e).lower() or "unauthorized" in str(e).lower()):
                print(f"Session error on attempt {attempt + 1}, refreshing context...")
                current_context = refresh_session(current_context)
                time.sleep(1)  # Brief delay before retry
            else:
                break
    
    assert last_exception is not None
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
