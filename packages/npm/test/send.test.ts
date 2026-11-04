import {afterEach, describe, expect, test} from 'vitest';
import {createServer, Server} from 'node:http';
import {AddressInfo} from 'node:net';
import {generateKeyPairSync} from 'node:crypto';
import {createConfig} from "../src/config";
import {rawHandler} from "../src/wirespec";

describe('send', () => {
    let server: Server;

    afterEach(() => new Promise(resolve => {
        server.closeAllConnections();
        server.close(resolve);
    }));

    test('a request without an answer within the request timeout rejects with a TimeoutError', async () => {
        server = createServer(() => {
            // never answers
        });
        await new Promise<void>(resolve => server.listen(0, '127.0.0.1', resolve));
        const baseUrl = `http://127.0.0.1:${(server.address() as AddressInfo).port}/`;
        const {privateKey, publicKey} = generateKeyPairSync('rsa', {
            modulusLength: 2048,
            privateKeyEncoding: {type: 'pkcs8', format: 'pem'},
            publicKeyEncoding: {type: 'spki', format: 'pem'},
        });
        const config = createConfig({baseUrl, pinnedKey: ''}, 'test', 'key', privateKey, publicKey, {requestTimeoutMs: 200});

        await expect(rawHandler(config, {method: 'GET', path: ['ping'], queries: {}, headers: {}, body: undefined}))
            .rejects.toMatchObject({name: 'TimeoutError'});
    });
});
