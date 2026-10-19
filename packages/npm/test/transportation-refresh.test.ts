import {afterEach, describe, expect, test} from 'vitest';
import {createServer, Server} from 'node:http';
import {AddressInfo} from 'node:net';
import {generateKeyPairSync} from 'node:crypto';
import {createConfig} from "../src/config";
import {respond, serverPublicKey, signBody} from "./server-key";
import {Context} from "../src/context";
import {transportation} from "../src/transportation";
import {Wirespec} from "../src/gen/Wirespec";
import {BunqApiError} from "../src/wirespec";

const authenticationError = '{"Error":[{"error_description":"Insufficient authentication."}]}';
const request: Wirespec.RawRequest = {method: 'GET', path: ['ping'], queries: {}, headers: {}, body: undefined};

describe('transportation session refresh', () => {
    let server: Server;
    let seenTokens: (string | undefined)[];

    afterEach(() => new Promise(resolve => server.close(resolve)));

    /** Set by `fresh`: like bunq, the server accepts the session again after a refresh although the token stays the same. */
    let revived: boolean;
    /** Set to false to make the server answer revived requests without a signature. */
    let signRetries = true;
    /** Answers the second request 400 ms late, so its 403 arrives after the first request's refresh has finished. */
    let slowSecondRequest: boolean;

    /** Answers 200 once revived, otherwise 403 with [rejection]. */
    async function contextRejectingWith(rejection: string, expiry = new Date(Date.now() + 3600_000)): Promise<Context> {
        seenTokens = [];
        revived = false;
        slowSecondRequest = false;
        signRetries = true;
        server = createServer((req, res) => {
            const token = req.headers['x-bunq-client-authentication'] as string | undefined;
            seenTokens.push(token);
            const ok = revived;
            setTimeout(() => {
                const body = ok ? '{"Response":[]}' : rejection;
                respond(res, ok ? 200 : 403, body, ok && !signRetries ? null : signBody(body));
            }, slowSecondRequest && seenTokens.length === 2 ? 400 : 0);
        });
        await new Promise<void>(resolve => server.listen(0, '127.0.0.1', resolve));
        const baseUrl = `http://127.0.0.1:${(server.address() as AddressInfo).port}/`;
        const {privateKey, publicKey} = generateKeyPairSync('rsa', {
            modulusLength: 2048,
            privateKeyEncoding: {type: 'pkcs8', format: 'pem'},
            publicKeyEncoding: {type: 'spki', format: 'pem'},
        });
        return {
            serverPublicKey, deviceId: 1, sessionId: 1, sessionToken: 'stale', userId: 1,
            sessionExpiryTime: expiry, installationToken: 'installation',
            config: createConfig({baseUrl, pinnedKey: ''}, 'test', 'key', privateKey, publicKey),
        };
    }

    /** What bunq returns for a re-created session: the same token with a later expiry. */
    const fresh = (context: Context): Context => {
        revived = true;
        return {...context, sessionExpiryTime: new Date(Date.now() + 3600_000)};
    };

    test('insufficient authentication refreshes once and retries with the new token', async () => {
        const context = await contextRejectingWith(authenticationError);
        let refreshes = 0;
        const transport = transportation(context, async ctx => { refreshes++; return fresh(ctx); });

        const response = await transport.transport(request);

        expect(response.statusCode).toBe(200);
        expect(refreshes).toBe(1);
        expect(seenTokens).toEqual(['stale', 'stale']);
    });

    test('an unsigned response after the refresh throws', async () => {
        const context = await contextRejectingWith(authenticationError);
        signRetries = false;
        const transport = transportation(context, async ctx => fresh(ctx));

        await expect(transport.transport(request)).rejects.toThrow('Invalid bunq server signature');
    });

    test('a failing refresh throws the original 403', async () => {
        const context = await contextRejectingWith(authenticationError);
        const transport = transportation(context, async () => { throw new Error('429'); });

        await expect(transport.transport(request)).rejects.toMatchObject({status: 403, body: authenticationError});
        expect(seenTokens).toEqual(['stale']);
    });

    test('a refresh that throws synchronously throws the original 403', async () => {
        const context = await contextRejectingWith(authenticationError);
        const transport = transportation(context, () => { throw new Error('boom'); });

        await expect(transport.transport(request)).rejects.toMatchObject({status: 403});
        expect(seenTokens).toEqual(['stale']);
    });

    test('another 403 does not refresh', async () => {
        const context = await contextRejectingWith('{"Error":[{"error_description":"You are not allowed to make this call."}]}');
        let refreshes = 0;
        const transport = transportation(context, async ctx => { refreshes++; return fresh(ctx); });

        await expect(transport.transport(request)).rejects.toBeInstanceOf(BunqApiError);
        expect(refreshes).toBe(0);
    });

    test('a 403 with an empty body does not refresh', async () => {
        const context = await contextRejectingWith('');
        let refreshes = 0;
        const transport = transportation(context, async ctx => { refreshes++; return fresh(ctx); });

        await expect(transport.transport(request)).rejects.toBeInstanceOf(BunqApiError);
        expect(refreshes).toBe(0);
    });

    test('a 403 with an HTML body throws and does not refresh', async () => {
        const context = await contextRejectingWith('<html>forbidden</html>');
        let refreshes = 0;
        const transport = transportation(context, async ctx => { refreshes++; return fresh(ctx); });

        await expect(transport.transport(request)).rejects.toMatchObject({status: 403, body: '<html>forbidden</html>'});
        expect(refreshes).toBe(0);
    });

    test('concurrent calls refresh once', async () => {
        const context = await contextRejectingWith(authenticationError);
        let refreshes = 0;
        const transport = transportation(context, async ctx => {
            await new Promise(resolve => setTimeout(resolve, 200));
            refreshes++;
            return fresh(ctx);
        });

        const responses = await Promise.all([transport.transport(request), transport.transport(request)]);

        expect(responses.map(response => response.statusCode)).toEqual([200, 200]);
        expect(refreshes).toBe(1);
    });

    test('an expired context is refreshed before the first request and the callback fires once', async () => {
        const context = await contextRejectingWith(authenticationError, new Date(Date.now() - 1000));
        let refreshes = 0;
        const changes: string[] = [];
        const transport = transportation(context, async ctx => { refreshes++; return fresh(ctx); }, ctx => { changes.push(ctx.sessionToken); });

        const response = await transport.transport(request);

        expect(response.statusCode).toBe(200);
        expect(refreshes).toBe(1);
        expect(seenTokens).toEqual(['stale']);
        expect(changes).toHaveLength(1);
    });

    test('a context that is not expired is not refreshed', async () => {
        const context = await contextRejectingWith(authenticationError);
        revived = true;
        let refreshes = 0;
        const transport = transportation(context, async ctx => { refreshes++; return ctx; }, () => { refreshes++; });

        expect((await transport.transport(request)).statusCode).toBe(200);

        expect(refreshes).toBe(0);
        expect(seenTokens).toEqual(['stale']);
    });

    test('a 403 refresh calls the callback once with the new context', async () => {
        const context = await contextRejectingWith(authenticationError);
        const changes: string[] = [];
        const transport = transportation(context, async ctx => fresh(ctx), ctx => { changes.push(ctx.sessionToken); });

        expect((await transport.transport(request)).statusCode).toBe(200);

        expect(changes).toHaveLength(1);
    });

    test('concurrent calls on an expired context refresh once when bunq keeps the session token', async () => {
        const context = await contextRejectingWith(authenticationError, new Date(Date.now() - 1000));
        let refreshes = 0;
        let changes = 0;
        const transport = transportation(context, async ctx => {
            await new Promise(resolve => setTimeout(resolve, 200));
            refreshes++;
            return fresh(ctx);
        }, () => { changes++; });

        const responses = await Promise.all([transport.transport(request), transport.transport(request), transport.transport(request)]);

        expect(responses.map(r => r.statusCode)).toEqual([200, 200, 200]);
        expect(refreshes).toBe(1);
        expect(changes).toBe(1);
    });

    test('a failed refresh before sending is not repeated after the 403', async () => {
        const context = await contextRejectingWith(authenticationError, new Date(Date.now() - 1000));
        let refreshes = 0;
        const transport = transportation(context, async () => { refreshes++; throw new Error('429'); });

        await expect(transport.transport(request)).rejects.toMatchObject({status: 403});
        expect(refreshes).toBe(1);
    });

    test('a context expiring in 10 seconds is refreshed', async () => {
        const context = await contextRejectingWith(authenticationError, new Date(Date.now() + 10_000));
        let refreshes = 0;
        const transport = transportation(context, async ctx => { refreshes++; return fresh(ctx); });

        expect((await transport.transport(request)).statusCode).toBe(200);
        expect(refreshes).toBe(1);
        expect(seenTokens).toEqual(['stale']); // refreshed before sending: no rejected request first
    });

    test('a 403 that arrives after another request refreshed reuses that refresh when bunq keeps the session token', async () => {
        const context = await contextRejectingWith(authenticationError);
        slowSecondRequest = true;
        let refreshes = 0;
        const transport = transportation(context, async ctx => {
            await new Promise(resolve => setTimeout(resolve, 50));
            refreshes++;
            return fresh(ctx);
        });

        const responses = await Promise.all([transport.transport(request), transport.transport(request)]);

        expect(responses.map(r => r.statusCode)).toEqual([200, 200]);
        expect(refreshes).toBe(1);
    });
});
