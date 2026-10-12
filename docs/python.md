# Python SDK

## Requirements

- Python 3.10+ (the generated code uses `match`/`case`)
- `httpx`, `cryptography` and `dacite` (see `packages/python/requirements.txt`)

The Python client is async-only: `init_context`, `refresh_session` and every client method are coroutines. Sync code can call them through `asyncio.run(...)`.

## Setup

The generated code in `packages/python/src/api` is not committed. Generate it, install the dependencies and put `packages/python/src` on your import path:

```bash
./gradlew :packages:python:wirespec
pip install -r packages/python/requirements.txt
export PYTHONPATH=packages/python/src
```

## Creating a Context

```python
from bunq_server import BUNQ_SANDBOX_SERVER
from bunq_signing_keys_generator import BunqSigningKeysGenerator
from config import create_config
from context import init_context

private_key_pem, public_key_pem = BunqSigningKeysGenerator.generate_bunq_signing_keys_as_pem()
config = create_config(
    bunq_server=BUNQ_SANDBOX_SERVER,
    service_name="MyApp",
    api_key="your-api-key",
    private_key_pem=private_key_pem,
    public_key_pem=public_key_pem,
)
```

`generate_bunq_signing_keys_as_pem()` creates a new key pair on every call. To keep the same keys across restarts, store the PEM strings, or use `BunqSigningKeysGenerator.generate_bunq_signing_keys_with_files(private_key_file, public_key_file)`, which reuses existing files or writes new ones.

## Creating the Client and Calling an Endpoint

`bunq_client(context)` returns the client that Wirespec generates. Its methods are `async` and named after the operation id in snake_case (`read_user`, `list_all_monetary_account_bank_for_user`). Pass `None` for query parameters you do not use. Match on the response class to read the typed body.

```python
import asyncio

from api.endpoint.ListAllMonetaryAccountBankForUser import Response200 as ListAccountsResponse200
from api.endpoint.ReadUser import Response200 as ReadUserResponse200
from wirespec import bunq_client


async def main():
    ctx = await init_context(config)
    client = bunq_client(ctx)

    user = await client.read_user(itemId=ctx.user_id)
    match user:
        case ReadUserResponse200(body=body):
            print(body.UserPerson.legal_name if body.UserPerson else None)
        case _:
            raise RuntimeError(user)

    accounts = await client.list_all_monetary_account_bank_for_user(
        userID=ctx.user_id, count=None, newer_id=None, older_id=None
    )
    match accounts:
        case ListAccountsResponse200(body=body):
            for account in body:
                print(account.display_name)
        case _:
            raise RuntimeError(accounts)


asyncio.run(main())
```

## Session Refresh

The client refreshes the session for you. When bunq answers with 403 "Insufficient authentication." (the response for an expired or deleted session), the client:

1. creates a new session once and retries the request with the new token, signed again;
2. shares that one refresh between concurrent calls (guarded by an `asyncio.Lock`), and uses the new token for later calls on the same client.

If the refresh fails, the original 403 response is returned and a warning is logged. Other 403 responses are returned unchanged. An endpoint whose spec lists no 403 response raises `Cannot match response with status: 403` when it receives one.

Keep using the same `bunq_client(ctx)` instance so that calls share the refreshed session.

### Manual Refresh

`refresh_session(context)` is still available. It creates a new session with the same device and installation and returns a new `Context`. An existing client does not pick it up; create a new client from the returned context:

```python
from context import refresh_session


async def refresh(ctx):
    refreshed_ctx = await refresh_session(ctx)
    return bunq_client(refreshed_ctx)
```

### Session Expiry Time

```python
from datetime import datetime, timedelta


def will_expire_soon(ctx) -> bool:
    return ctx.session_expiry_time < datetime.now() + timedelta(minutes=5)
```

## Context Properties

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

`init_context` and `refresh_session` raise an exception if session creation fails:

```python
async def create_context_or_none():
    try:
        return await init_context(config)
    except Exception as error:
        print(f"Session creation failed: {error}")
        return None
```
