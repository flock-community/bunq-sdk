import {afterEach, describe, expect, test} from 'vitest';
import {createServer, Server} from 'node:http';
import {AddressInfo} from 'node:net';
import {generateKeyPairSync} from 'node:crypto';
import {createConfig} from "../src/config";
import {Context, initContext, refreshSession} from "../src/context";
import {Signing} from "../src/signing";
import {transportation} from "../src/transportation";
import {respond, serverPublicKey, signBody} from "./server-key";

describe('response signatures', () => {
    let server: Server;

    afterEach(() => new Promise(resolve => server.close(resolve)));

    const body = '{"Response":[]}';

    async function call(status: number, responseBody: string, signature: string | null) {
        server = createServer((req, res) => respond(res, status, responseBody, signature));
        await new Promise<void>(resolve => server.listen(0, '127.0.0.1', resolve));
        const baseUrl = `http://127.0.0.1:${(server.address() as AddressInfo).port}/`;
        const {privateKey, publicKey} = generateKeyPairSync('rsa', {
            modulusLength: 2048,
            privateKeyEncoding: {type: 'pkcs8', format: 'pem'},
            publicKeyEncoding: {type: 'spki', format: 'pem'},
        });
        const context: Context = {
            serverPublicKey, deviceId: 1, sessionId: 1, sessionToken: 'token', userId: 1,
            sessionExpiryTime: new Date(Date.now() + 3600_000), installationToken: 'installation',
            config: createConfig({baseUrl, pinnedKey: ''}, 'test', 'key', privateKey, publicKey),
        };
        return transportation(context).transport({method: 'GET', path: ['ping'], queries: {}, headers: {}, body: undefined});
    }

    test('a valid signature passes', async () => {
        expect((await call(200, body, signBody(body))).statusCode).toBe(200);
    });

    test('a valid signature on a 400 passes', async () => {
        const error = '{"Error":[{"error_description":"x"}]}';
        expect((await call(400, error, signBody(error))).statusCode).toBe(400);
    });

    test('a 400 with an invalid signature throws', async () => {
        await expect(call(400, '{"Error":[{"error_description":"x"}]}', signBody('other'))).rejects.toThrow('Invalid bunq server signature');
    });

    test('a 400 with a missing signature throws', async () => {
        await expect(call(400, '{"Error":[{"error_description":"x"}]}', null)).rejects.toThrow('Invalid bunq server signature');
    });

    test('a signature over another body throws', async () => {
        await expect(call(200, body, signBody('other'))).rejects.toThrow('Invalid bunq server signature');
    });

    test('a missing signature throws', async () => {
        await expect(call(200, body, null)).rejects.toThrow('Invalid bunq server signature');
    });

    test('a signature that is not base64 throws', async () => {
        await expect(call(200, body, 'not base64!')).rejects.toThrow('Invalid bunq server signature');
    });

    test('verifyResponse checks the raw body bytes', () => {
        const bytes = new TextEncoder().encode('{"a": 1}\n');
        const signature = signBody(bytes);
        expect(Signing.verifyResponse(serverPublicKey, bytes, signature)).toBe(true);
        expect(Signing.verifyResponse(serverPublicKey, new TextEncoder().encode('{"a":1}'), signature)).toBe(false);
        expect(Signing.verifyResponse(serverPublicKey, bytes, undefined)).toBe(false);
    });

    const sessionBody = '{"Response":[{"Id":{"id":1}},{"Token":{"token":"t"}},{"UserApiKey":{"id":2}}]}';

    async function context(handler: (url: string) => [string, string | null]): Promise<Context> {
        server = createServer((req, res) => {
            const [responseBody, signature] = handler(req.url ?? '');
            respond(res, 200, responseBody, signature);
        });
        await new Promise<void>(resolve => server.listen(0, '127.0.0.1', resolve));
        const baseUrl = `http://127.0.0.1:${(server.address() as AddressInfo).port}/`;
        const {privateKey, publicKey} = generateKeyPairSync('rsa', {
            modulusLength: 2048,
            privateKeyEncoding: {type: 'pkcs8', format: 'pem'},
            publicKeyEncoding: {type: 'spki', format: 'pem'},
        });
        return {
            serverPublicKey, deviceId: 1, sessionId: 1, sessionToken: 'token', userId: 1,
            sessionExpiryTime: new Date(Date.now() + 3600_000), installationToken: 'installation',
            config: createConfig({baseUrl, pinnedKey: ''}, 'test', 'key', privateKey, publicKey),
        };
    }

    test('refreshSession with an empty server public key throws instead of accepting an unsigned response', async () => {
        const ctx = await context(() => [sessionBody, null]);
        await expect(refreshSession({...ctx, serverPublicKey: ''})).rejects.toThrow('Invalid bunq server signature');
    });

    test('initContext throws on an unsigned device server response', async () => {
        const installation = JSON.stringify({Response: [{Id: {id: 1}}, {Token: {token: 't'}}, {ServerPublicKey: {server_public_key: serverPublicKey}}]});
        const ctx = await context(url => url.includes('installation') ? [installation, null] : ['{"Response":[{"Id":{"id":3}}]}', null]);
        await expect(initContext(ctx.config)).rejects.toThrow('Invalid bunq server signature');
    });
});
