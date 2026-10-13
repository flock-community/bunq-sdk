# Python SDK

## Requirements

- Python 3.10+ (the generated code uses `match`/`case`)
- JDK 17+ to run the Gradle code generation (CI uses 21)
- `httpx`, `cryptography` and `dacite` (see `packages/python/requirements.txt`)

The Python client is async-only: `init_context`, `refresh_session` and every client method are coroutines. Sync code can call them through `asyncio.run(...)`.

## Setup

The generated code in `packages/python/src/api` is not committed. Generate it, install the dependencies and put `packages/python/src` on your import path (run this from the repository root):

```bash
./gradlew :packages:python:wirespec
pip install -r packages/python/requirements.txt
export PYTHONPATH="$(pwd)/packages/python/src"
```

The modules are top-level (`config`, `context`, `wirespec`, ...), so a `config.py` or `context.py` in your own project shadows them.

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

from api.endpoint.ListAllMonetaryAccountBankForUser import (
    Response200 as ListAccountsResponse200,
    ResponseGenericError as ListAccountsError,
)
from api.endpoint.ReadUser import Response200 as ReadUserResponse200, ResponseGenericError as ReadUserError
from wirespec import bunq_client


async def main():
    ctx = await init_context(config)
    client = bunq_client(ctx)

    user = await client.read_user(itemId=ctx.user_id)
    match user:
        case ReadUserResponse200(body=body):
            print(body.UserPerson.legal_name if body.UserPerson else None)
        case ReadUserError(status=status, body=error):
            raise RuntimeError(f"bunq answered {status}: {error.Error}")

    accounts = await client.list_all_monetary_account_bank_for_user(
        userID=ctx.user_id, count=None, newer_id=None, older_id=None
    )
    match accounts:
        case ListAccountsResponse200(body=body):
            for account in body:
                print(account.display_name)
        case ListAccountsError(status=status, body=error):
            raise RuntimeError(f"bunq answered {status}: {error.Error}")


asyncio.run(main())
```

## Session Refresh

See [Session Refresh in the README](../README.md#session-refresh) for how the client refreshes the session, what happens when the refresh fails (the call returns `Response403`), and the manual refresh.

The shared refresh is guarded by an `asyncio.Lock`, and the refresh-failure warning is logged through the `logging` module (logger name `wirespec`). Keep using the same `bunq_client(ctx)` instance.

### Manual Refresh

`refresh_session(context)` creates a new session with the same device and installation and returns a new `Context`. An existing client does not pick it up; create a new client from the returned context:

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

See [Error Handling in the README](../README.md#error-handling) for the error statuses and the cases that throw.

Typed error responses are returned, not raised. `ResponseGenericError` is the common class of all error statuses (`Response400`, `Response403`, ...) and its body is a `GenericError`. The `case ReadUserError(...)` branches above match all of them; `case _:` also matches, but loses the type of `body`.

A status outside the list (for example 502) raises `Exception("Cannot match response with status: 502")`, and a non-JSON error body raises `bunq answered 502 with a non-JSON body: ...`.

`init_context` and `refresh_session` raise an exception if session creation fails, with a message like `Session server creation failed (status 400): <error_description>`:

```python
async def create_context_or_none():
    try:
        return await init_context(config)
    except Exception as error:
        print(f"Session creation failed: {error}")
        return None
```
