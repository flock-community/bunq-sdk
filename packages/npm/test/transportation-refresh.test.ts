import {afterEach, describe, expect, test} from 'vitest';
import {createServer, Server} from 'node:http';
import {AddressInfo} from 'node:net';
import {generateKeyPairSync} from 'node:crypto';
import {createConfig} from "../src/config";
import {Context} from "../src/context";
import {transportation} from "../src/transportation";
import {Wirespec} from "../src/gen/Wirespec";

const authenticationError = '{"Error":[{"error_description":"Insufficient authentication."}]}';
const request: Wirespec.RawRequest = {method: 'GET', path: ['ping'], queries: {}, headers: {}, body: undefined};

describe('transportation session refresh', () => {
    let server: Server;
    let seenTokens: (string | undefined)[];

    afterEach(() => new Promise(resolve => server.close(resolve)));

    /** Answers 200 for the token "fresh", otherwise 403 with [rejection]. */
    async function contextRejectingWith(rejection: string): Promise<Context> {
        seenTokens = [];
        server = createServer((req, res) => {
            const token = req.headers['x-bunq-client-authentication'] as string | undefined;
            seenTokens.push(token);
            res.statusCode = token === 'fresh' ? 200 : 403;
            res.end(token === 'fresh' ? '{}' : rejection);
        });
        await new Promise<void>(resolve => server.listen(0, '127.0.0.1', resolve));
        const baseUrl = `http://127.0.0.1:${(server.address() as AddressInfo).port}/`;
        const {privateKey, publicKey} = generateKeyPairSync('rsa', {
            modulusLength: 2048,
            privateKeyEncoding: {type: 'pkcs8', format: 'pem'},
            publicKeyEncoding: {type: 'spki', format: 'pem'},
        });
        return {
            serverPublicKey: '', deviceId: 1, sessionId: 1, sessionToken: 'stale', userId: 1,
            sessionExpiryTime: new Date(), installationToken: 'installation',
            config: createConfig({baseUrl, pinnedKey: ''}, 'test', 'key', privateKey, publicKey),
        };
    }

    const fresh = (context: Context): Context => ({...context, sessionToken: 'fresh'});

    test('insufficient authentication refreshes once and retries with the new token', async () => {
        const context = await contextRejectingWith(authenticationError);
        let refreshes = 0;
        const transport = transportation(context, async ctx => { refreshes++; return fresh(ctx); });

        const response = await transport.transport(request);

        expect(response.statusCode).toBe(200);
        expect(refreshes).toBe(1);
        expect(seenTokens).toEqual(['stale', 'fresh']);
    });

    test('a failing refresh returns the original 403', async () => {
        const context = await contextRejectingWith(authenticationError);
        const transport = transportation(context, async () => { throw new Error('429'); });

        const response = await transport.transport(request);

        expect(response.statusCode).toBe(403);
        expect(seenTokens).toEqual(['stale']);
    });

    test('a refresh that throws synchronously returns the original 403', async () => {
        const context = await contextRejectingWith(authenticationError);
        const transport = transportation(context, () => { throw new Error('boom'); });

        expect((await transport.transport(request)).statusCode).toBe(403);
        expect(seenTokens).toEqual(['stale']);
    });

    test('another 403 does not refresh', async () => {
        const context = await contextRejectingWith('{"Error":[{"error_description":"You are not allowed to make this call."}]}');
        let refreshes = 0;
        const transport = transportation(context, async ctx => { refreshes++; return fresh(ctx); });

        expect((await transport.transport(request)).statusCode).toBe(403);
        expect(refreshes).toBe(0);
    });

    test('a 403 with an empty body does not refresh', async () => {
        const context = await contextRejectingWith('');
        let refreshes = 0;
        const transport = transportation(context, async ctx => { refreshes++; return fresh(ctx); });

        expect((await transport.transport(request)).statusCode).toBe(403);
        expect(refreshes).toBe(0);
    });

    test('a 403 with an HTML body fails naming the status and does not refresh', async () => {
        const context = await contextRejectingWith('<html>forbidden</html>');
        let refreshes = 0;
        const transport = transportation(context, async ctx => { refreshes++; return fresh(ctx); });

        await expect(transport.transport(request)).rejects.toThrow(/403.*<html>forbidden<\/html>/);
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
});
