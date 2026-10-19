# Python SDK

## Requirements

- Python 3.10+ (the generated code uses `match`/`case`)
- JDK 17+ to run the Gradle code generation (CI uses 21)
- `httpx`, `cryptography` and `dacite` (see `packages/python/requirements.txt`)

The Python client is async-only: `init_context`, `refresh_session` and every client method are coroutines. Sync code can call them through `asyncio.run(...)`.

## Setup

The package is not published to PyPI, and the generated code in `packages/python/src/api` is not committed. Generate it, install the dependencies and put `packages/python/src` on your import path (run this from the repository root):

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

`bunq_client(context)` returns the client that Wirespec generates. Its methods are `async` and named after the operation id in snake_case (`read_user`, `list_all_monetary_account_bank_for_user`). Pass `None` for query parameters you do not use. Match on the response class (`Response200` or `Response400`) to read the typed body. Any other status raises `BunqApiError` (see Error Handling).

```python
import asyncio

from api.endpoint.ListAllMonetaryAccountBankForUser import (
    Response200 as ListAccountsResponse200,
    Response400 as ListAccountsResponse400,
)
from api.endpoint.ReadUser import Response200 as ReadUserResponse200, Response400 as ReadUserResponse400
from wirespec import bunq_client


async def main():
    ctx = await init_context(config)
    client = bunq_client(ctx)

    user = await client.read_user(itemId=ctx.user_id)
    match user:
        case ReadUserResponse200(body=body):
            print(body.UserPerson.legal_name if body.UserPerson else None)
        case ReadUserResponse400(body=error):
            raise RuntimeError(f"Received 400: {error.Error}")

    accounts = await client.list_all_monetary_account_bank_for_user(
        userID=ctx.user_id, count=None, newer_id=None, older_id=None
    )
    match accounts:
        case ListAccountsResponse200(body=body):
            for account in body:
                print(account.display_name)
        case ListAccountsResponse400(body=error):
            raise RuntimeError(f"Received 400: {error.Error}")


asyncio.run(main())
```

## Session Refresh

See [Session Refresh in the README](../README.md#session-refresh) for how the client refreshes the session, what happens when the refresh fails (the call raises `BunqApiError` with status 403), and the manual refresh.

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

## Persist and restore a Context

`init_context` registers an installation and a device, which you only need once per API key. Store the `Context` and build the client from it on the next start instead of calling `init_context` again.

Store every field of `Context`: `server_public_key`, `device_id`, `session_id`, `session_token`, `user_id`, `session_expiry_time`, `installation_token` and the secrets in `config` (API key and signing keys). The SDK has no serialisation format of its own. Treat the stored data as a secret and store it encrypted (see the masking note under Context Properties).

Pass `on_context_change` to `bunq_client` to receive the new `Context` after every refresh, whether triggered by a 403 or by expiry. It is called once per refresh. If it throws, the exception reaches the caller of the request that triggered the refresh.

```python
# first start
context = await init_context(config)
save(context)

# later starts: build the Context from the stored fields (config is supplied again by your code)
restored = Context(
    server_public_key=stored["server_public_key"],
    device_id=stored["device_id"],
    session_id=stored["session_id"],
    session_token=stored["session_token"],
    user_id=stored["user_id"],
    session_expiry_time=datetime.fromisoformat(stored["session_expiry_time"]),
    installation_token=stored["installation_token"],
    config=config,
)
client = bunq_client(restored, on_context_change=save)  # a plain function, not a coroutine
```

If `session_expiry_time` is in the past or less than 30 seconds away, the client refreshes the session before the first request, so a stored context that expired while the app was stopped works. Concurrent calls share one refresh. If that refresh fails, the request is sent with the old token; if bunq answers 403 "Insufficient authentication.", that 403 is returned as the error without a second refresh. If bunq no longer accepts the stored installation or device, the refresh fails; call `init_context` again. `session_expiry_time` is a naive local `datetime` when created by `init_context`; a timezone-aware value is compared in its own zone.

## Logging

The SDK logs through the standard `logging` module, with one logger per module (for example `wirespec`, `context`, `signing`). Configure them with `logging.getLogger("<module>")`.

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

`repr()` of `Context` and `Config` masks secrets; the object still holds them, so store it encrypted.

## Response Signatures

bunq signs every response: the `X-Bunq-Server-Signature` header holds a base64 SHA256withRSA (PKCS#1 v1.5) signature over the raw response body bytes. Every 200 and 400 response that reaches the generated client is verified against `context.server_public_key`, the server public key bunq returned when the installation was created. The requests of `init_context` after the installation are verified with that key as well.

A response without the header, or with a signature that does not match the body, is rejected with `Exception("Invalid bunq server signature")`; the coroutine raises, also for `init_context` and `refresh_session`. Other statuses (403, 404, 5xx, ...) are thrown as the API error described under Error Handling before the signature is looked at.

The installation response itself is not verified: the key it carries is not known yet, so it only proves that the sender holds the key it announces. The pinned certificate of the `BunqServer` is what protects that call.

## Error Handling

See [Error Handling in the README](../README.md#error-handling) for when the error is raised.

A 400 is returned as `Response400`, whose body has `Error` (a list with an `error_description` per entry). Every other outcome raises `BunqApiError` (`from transport import BunqApiError`), which has `status` and `body`, the full response body as a string; the message is `Received <status>: <first 500 characters>`:

```python
from api.endpoint.ReadUser import Response200 as ReadUserResponse200, Response400 as ReadUserResponse400
from transport import BunqApiError


async def read_legal_name(client, user_id: int):
    try:
        match await client.read_user(itemId=user_id):
            case ReadUserResponse200(body=body):
                return body.UserPerson.legal_name if body.UserPerson else None
            case ReadUserResponse400(body=error):
                raise RuntimeError(f"Received 400: {error.Error}")
    except BunqApiError as e:
        if e.status == 404:
            return None
        raise
```

`init_context` and `refresh_session` raise an exception if session creation fails. A typed 400 gives a message like `Session server creation failed (status 400): <error_description>` (the steps are "Installation failed", "Device server creation failed" and "Session server creation failed"); any other status raises `BunqApiError`:

```python
async def create_context_or_none():
    try:
        return await init_context(config)
    except Exception as error:
        print(f"Session creation failed: {error}")
        return None
```
