# TypeScript/npm SDK

## Overview

The package exports `bunqClient`, `initContext`, `refreshSession`, `createConfig` and the generated models and endpoints from one entry point.

## Requirements

- Node.js 18+ (global `fetch`; CI uses Node 20)
- TypeScript 5; the code on this page is type-checked with `strict` enabled
- JDK 17+ to run the Gradle code generation (CI uses 21)

## Install

There is no versioned release yet. Build and pack the package, then install the tarball in your project:

```bash
./gradlew :packages:npm:wirespec
npm --prefix packages/npm install
npm pack ./packages/npm
npm install /path/to/bunq-sdk/bunq-sdk-1.0.0.tgz   # run in your project
```

## Creating a Context

```typescript
import {BUNQ_SANDBOX_SERVER, createConfig, initContext} from "bunq-sdk";
import {generateKeyPairSync} from "node:crypto";

const {privateKey, publicKey} = generateKeyPairSync("rsa", {
  modulusLength: 2048,
  privateKeyEncoding: {type: "pkcs8", format: "pem"},
  publicKeyEncoding: {type: "spki", format: "pem"},
});

const config = createConfig(BUNQ_SANDBOX_SERVER, "MyApp", "your-api-key", privateKey, publicKey);
```

The package is CommonJS and has no top-level `await`: call `initContext` and the client from inside `async function main() { ... } main();`, as in the next section.

Generate the key pair once and store it: a new pair means a new installation at bunq. `createConfig` takes an optional last argument `{userAgent, cacheControl, language, region, clientRequestId, geolocation}`.

## Creating the Client and Calling an Endpoint

`bunqClient(context)` returns the client that Wirespec generates. Its methods are `async` and named after the operation id in camelCase (`readUser`, `listAllMonetaryAccountBankForUser`). The result is a response object with a `status`; narrow on it to read the typed `body`.

```typescript
import {bunqClient} from "bunq-sdk";

async function main() {
  const context = await initContext(config);
  const client = bunqClient(context);

  const user = await client.readUser({itemId: context.userId});
  if (user.status === 200) {
    console.log(user.body.UserPerson?.legal_name);
  } else {
    console.error(user.status, user.body.Error?.map(error => error.error_description));
  }

  const accounts = await client.listAllMonetaryAccountBankForUser({userID: context.userId});
  if (accounts.status === 200) {
    accounts.body.forEach(account => console.log(account.display_name));
  } else {
    console.error(accounts.status, accounts.body.Error?.map(error => error.error_description));
  }
}

main();
```

The optional query parameters (`count`, `newer_id`, `older_id`) can be left out.

## Session Refresh

See [Session Refresh in the README](../README.md#session-refresh) for how the client refreshes the session, what happens when the refresh fails (the call returns a response with `status === 403`), and the manual refresh.

Concurrent calls share one in-flight refresh promise, and the refresh-failure warning is logged with `console.warn`. Keep using the same `bunqClient(context)` instance.

### Manual Refresh

`refreshSession(context)` is still available. It creates a new session with the same device and installation and returns a new `Context`. An existing client does not pick it up; create a new client from the returned context:

```typescript
import {bunqClient, type Context, refreshSession} from "bunq-sdk";

async function refresh(context: Context) {
  const refreshedContext = await refreshSession(context);
  return bunqClient(refreshedContext);
}
```

### Session Expiry Time

```typescript
const expiryTime: Date = context.sessionExpiryTime;
const willExpireSoon = expiryTime.getTime() < Date.now() + 5 * 60 * 1000;
```

## Context Properties

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

See [Error Handling in the README](../README.md#error-handling) for the error statuses and the cases that throw.

Typed error responses are returned, not thrown. When `status` is not 200, `body` is a `GenericError`:

```typescript
import {type BunqClient} from "bunq-sdk";

async function readLegalName(client: BunqClient, userId: number) {
  const res = await client.readUser({itemId: userId});
  if (res.status === 200) {
    return res.body.UserPerson?.legal_name;
  }
  if (res.status === 404) {
    return undefined;
  }
  throw new Error(`bunq answered ${res.status}: ${res.body.Error?.[0]?.error_description}`);
}
```

A status outside the list (for example 502) rejects with `Error('Cannot match response with status:')` (the TypeScript emitter of Wirespec 0.21.1 omits the status number), and a non-JSON error body rejects with `bunq answered 502 with a non-JSON body: ...`.

`initContext` and `refreshSession` reject if session creation fails, with a message like `Session server creation failed (status 400): <error_description>`:

```typescript
async function createContextOrUndefined() {
  try {
    return await initContext(config);
  } catch (error) {
    console.error("Session creation failed:", (error as Error).message);
    return undefined;
  }
}
```
