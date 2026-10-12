import {afterEach, describe, expect, test} from 'vitest';
import {createServer, IncomingHttpHeaders, Server} from 'node:http';
import {AddressInfo} from 'node:net';
import {generateKeyPairSync} from 'node:crypto';
import {rawHandler} from "../src/wirespec";
import {createConfig} from "../src/config";

describe('User-Agent header', () => {
    let server: Server;

    afterEach(() => new Promise(resolve => server.close(resolve)));

    async function userAgentSentFor(options?: { userAgent?: string }) {
        let received: IncomingHttpHeaders = {};
        server = createServer((req, res) => {
            received = req.headers;
            res.end();
        });
        await new Promise<void>(resolve => server.listen(0, '127.0.0.1', resolve));
        const baseUrl = `http://127.0.0.1:${(server.address() as AddressInfo).port}/`;
        const {privateKey, publicKey} = generateKeyPairSync('rsa', {
            modulusLength: 2048,
            privateKeyEncoding: {type: 'pkcs8', format: 'pem'},
            publicKeyEncoding: {type: 'spki', format: 'pem'},
        });
        const config = createConfig({baseUrl, pinnedKey: ''}, 'my-service', 'key', privateKey, publicKey, options);

        await rawHandler(config, {method: 'GET', path: ['ping'], queries: {}, headers: {}, body: undefined});

        return received['user-agent'];
    }

    test('defaults to the service name', async () => {
        expect(await userAgentSentFor()).toBe('my-service');
    });

    test('uses the configured user agent', async () => {
        expect(await userAgentSentFor({userAgent: 'my-agent'})).toBe('my-agent');
    });
});
