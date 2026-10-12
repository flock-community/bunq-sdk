# TypeScript/npm SDK

## Overview

`src/gen` is generated and not committed: run `./gradlew :packages:npm:wirespec` before `npm run build` or `npm test` in `packages/npm`.

The package exports `bunqClient`, `initContext`, `refreshSession`, `createConfig` and the generated models and endpoints from one entry point.

## Requirements

- Node.js with a global `fetch` (CI uses Node 20)
- TypeScript 5 with `strict` enabled (the package is type-checked that way)

## Install

There is no versioned release yet. Build and pack the package, then install the tarball in your project:

```bash
./gradlew :packages:npm:wirespec
npm --prefix packages/npm install
npm pack ./packages/npm
npm install ./bunq-sdk-1.0.0.tgz
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
const context = await initContext(config);
```

Generate the key pair once and store it: a new pair means a new installation at bunq. `createConfig` takes an optional last argument `{userAgent, cacheControl, language, region, clientRequestId, geolocation}`.

## Creating the Client and Calling an Endpoint

`bunqClient(context)` returns the client that Wirespec generates. Its methods are `async` and named after the operation id in camelCase (`readUser`, `listAllMonetaryAccountBankForUser`). The result is a response object with a `status`; narrow on it to read the typed `body`.

```typescript
import {bunqClient} from "bunq-sdk";

const client = bunqClient(context);

const user = await client.readUser({itemId: context.userId});
if (user.status === 200) {
  console.log(user.body.UserPerson?.legal_name);
}

const accounts = await client.listAllMonetaryAccountBankForUser({
  userID: context.userId,
  count: undefined,
  newer_id: undefined,
  older_id: undefined,
});
if (accounts.status === 200) {
  accounts.body.forEach(account => console.log(account.display_name));
}
```

## Session Refresh

The client refreshes the session for you. When bunq answers with 403 "Insufficient authentication." (the response for an expired or deleted session), the client:

1. creates a new session once and retries the request with the new token, signed again;
2. shares that one refresh between concurrent calls, and uses the new token for later calls on the same client.

If the refresh fails, the original 403 response is returned and a warning is logged with `console.warn`. Other 403 responses are returned unchanged.

Keep using the same `bunqClient(context)` instance so that calls share the refreshed session.

### Manual Refresh

`refreshSession(context)` is still available. It creates a new session with the same device and installation and returns a new `Context`. An existing client does not pick it up; create a new client from the returned context:

```typescript
import {refreshSession} from "bunq-sdk";

const refreshedContext = await refreshSession(context);
const refreshedClient = bunqClient(refreshedContext);
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

`initContext` and `refreshSession` reject if session creation fails:

```typescript
try {
  const context = await initContext(config);
} catch (error) {
  console.error("Session creation failed:", (error as Error).message);
}
```
