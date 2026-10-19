# TypeScript/npm SDK

## Overview

The package exports `bunqClient`, `initContext`, `refreshSession`, `createConfig` and the generated models and endpoints from one entry point.

## Requirements

- Node.js 18+ (global `fetch`; CI uses Node 20)
- TypeScript 5; the code on this page is type-checked with `strict` enabled
- JDK 17+ to run the Gradle code generation (CI uses 21)

## Install

The package is not published to npm. Build and pack the package, then install the tarball in your project:

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

`bunqClient(context)` returns the client that Wirespec generates. Its methods are `async` and named after the operation id in camelCase (`readUser`, `listAllMonetaryAccountBankForUser`). The result is a response object with a `status` of 200 or 400; narrow on it to read the typed `body`. Any other status rejects with `BunqApiError` (see Error Handling).

```typescript
import {bunqClient} from "bunq-sdk";

async function main() {
  const context = await initContext(config);
  const client = bunqClient(context);

  const user = await client.readUser({itemId: context.userId});
  if (user.status === 200) {
    console.log(user.body.UserPerson?.legal_name);
  } else {
    console.error(user.body.Error?.map(error => error.error_description));
  }

  const accounts = await client.listAllMonetaryAccountBankForUser({userID: context.userId});
  if (accounts.status === 200) {
    accounts.body.Response.forEach(account => console.log(account.display_name));
  } else {
    console.error(accounts.body.Error?.map(error => error.error_description));
  }
}

main();
```

The optional query parameters (`count`, `newer_id`, `older_id`) can be left out.

## Pagination

A list operation returns a page, `<Item>Page` (for example `PaymentPage`), with the items in `Response` and bunq's `Pagination` block in `Pagination`. `Pagination` has `future_url`, `newer_url` and `older_url`; each is null when there is nothing to follow. Items are listed newest first. To read the next (older) page, call the operation again with `older_id` set to the id of the last item of the current page. That is the `older_id` in `older_url`. When `older_url` is null there are no older items. The generated TypeScript type of the `*_url` fields is `string | undefined`, but the value is `null` at runtime, so check with `!older_url` and not with `=== undefined`. `newer_id` goes the other way: pass the id of the first item to get the items newer than it. `count` is the page size (at most 200).

```typescript
async function allPayments(client: BunqClient, userID: number, monetaryAccountID: number) {
  const payments = [];
  let olderId: number | undefined;
  do {
    const res = await client.listAllPaymentForUserMonetaryAccount({userID, monetaryAccountID, count: 200, newer_id: undefined, older_id: olderId});
    if (res.status !== 200) {
      throw new Error(res.body.Error?.[0]?.error_description);
    }
    payments.push(...res.body.Response);
    olderId = res.body.Pagination.older_url ? res.body.Response[res.body.Response.length - 1]?.id : undefined;
  } while (olderId !== undefined);
  return payments;
}
```

## Session Refresh

See [Session Refresh in the README](../README.md#session-refresh) for how the client refreshes the session, what happens when the refresh fails (the call rejects with `BunqApiError` with status 403), and the manual refresh.

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

## Persist and restore a Context

`initContext` registers an installation and a device, which you only need once per API key. Store the `Context` and build the client from it on the next start instead of calling `initContext` again.

Store every field of `Context`: `serverPublicKey`, `deviceId`, `sessionId`, `sessionToken`, `userId`, `sessionExpiryTime`, `installationToken` and the secrets in `config` (API key and signing keys). The SDK has no serialisation format of its own. Treat the stored data as a secret and store it encrypted (see the masking note under Context Properties).

Pass `onContextChange` to `bunqClient` to receive the new `Context` after every refresh, whether triggered by a 403 or by expiry. It is called once per refresh. If it throws, the exception reaches the caller of the request that triggered the refresh. It rejects the shared refresh, so every request waiting for that refresh rejects with the same error.

```typescript
// first start
const context = await initContext(config);
save(context);

// later starts: build the Context from the stored fields (config is supplied again by your code)
const restored: Context = {
  serverPublicKey: stored.serverPublicKey,
  deviceId: stored.deviceId,
  sessionId: stored.sessionId,
  sessionToken: stored.sessionToken,
  userId: stored.userId,
  sessionExpiryTime: new Date(stored.sessionExpiryTime), // a Date becomes a string in JSON
  installationToken: stored.installationToken,
  config,
};
const client = bunqClient(restored, updated => save(updated));
```

If `sessionExpiryTime` is in the past or less than 30 seconds away, the client refreshes the session before the first request, so a stored context that expired while the app was stopped works. Concurrent calls share one refresh. If that refresh fails, the request is sent with the old token; if bunq answers 403 "Insufficient authentication.", that 403 is returned as the error without a second refresh. If bunq no longer accepts the stored installation or device, the refresh fails; call `initContext` again.

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

`Context` and `Config` are plain objects, so logging them or calling `JSON.stringify` prints the secrets. Use `describeContext(context)` / `describeConfig(config)` for a masked string. The object still holds the secrets, so store it encrypted.

## Response Signatures

bunq signs every response: the `X-Bunq-Server-Signature` header holds a base64 SHA256withRSA (PKCS#1 v1.5) signature over the raw response body bytes. Every 200 and 400 response that reaches the generated client is verified against `context.serverPublicKey`, the server public key bunq returned when the installation was created. The requests of `initContext` after the installation are verified with that key as well.

A response without the header, or with a signature that does not match the body, is rejected with `Error("Invalid bunq server signature")`; the promise rejects, also for `initContext` and `refreshSession`. Other statuses (403, 404, 5xx, ...) are thrown as the API error described under Error Handling before the signature is looked at.

The installation response itself is not verified: the key it carries is not known yet, so it only proves that the sender holds the key it announces. The pinned certificate of the `BunqServer` is what protects that call.

## Error Handling

See [Error Handling in the README](../README.md#error-handling) for when the error is thrown.

A 400 is returned as a response with `status === 400`, whose `body` has `Error[]` with an `error_description` per entry. Every other outcome rejects with `BunqApiError` (exported from `bunq-sdk`), which has `status` and `body`, the full response body as a string; the message is `Received <status>: <first 500 characters>`:

```typescript
import {BunqApiError, type BunqClient} from "bunq-sdk";

async function readLegalName(client: BunqClient, userId: number) {
  try {
    const res = await client.readUser({itemId: userId});
    if (res.status === 200) {
      return res.body.UserPerson?.legal_name;
    }
    throw new Error(`Received 400: ${res.body.Error?.[0]?.error_description}`);
  } catch (error) {
    if (error instanceof BunqApiError && error.status === 404) {
      return undefined;
    }
    throw error;
  }
}
```

`initContext` and `refreshSession` reject if session creation fails. A typed 400 gives a message like `Session server creation failed (status 400): <error_description>` (the steps are "Installation failed", "Device server creation failed" and "Session server creation failed"); any other status gives a `BunqApiError`:

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
