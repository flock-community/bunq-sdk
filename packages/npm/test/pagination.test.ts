import {afterEach, describe, expect, test} from 'vitest';
import {createServer, Server} from 'node:http';
import {AddressInfo} from 'node:net';
import {generateKeyPairSync} from 'node:crypto';
import {createConfig} from "../src/config";
import {Context} from "../src/context";
import {respond, serverPublicKey} from "./server-key";
import {bunqClient} from "../src/transportation";

describe('list pagination', () => {
    let server: Server;

    afterEach(() => new Promise(resolve => server.close(resolve)));

    async function listAnswering(body: string) {
        server = createServer((req, res) => {
            respond(res, 200, body);
        });
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
        return bunqClient(context).listAllMonetaryAccountBankForUser({
            userID: 1, count: 2, newer_id: undefined, older_id: undefined,
        });
    }

    test('a list response keeps the items and the Pagination block', async () => {
        const response = await listAnswering(JSON.stringify({
            Response: [{MonetaryAccountBank: {id: 2, description: 'second'}}, {MonetaryAccountBank: {id: 1, description: 'first'}}],
            Pagination: {future_url: '/v1/future?newer_id=2', newer_url: null, older_url: '/v1/older?older_id=1'},
        }));

        expect(response.status).toBe(200);
        if (response.status !== 200) return;
        expect(response.body.Response.map(item => item.id)).toEqual([2, 1]);
        expect(response.body.Pagination).toEqual({future_url: '/v1/future?newer_id=2', newer_url: null, older_url: '/v1/older?older_id=1'});
    });

    test('an empty page has an empty list and its Pagination', async () => {
        const response = await listAnswering('{"Response":[],"Pagination":{"future_url":null,"newer_url":null,"older_url":null}}');

        expect(response.status).toBe(200);
        if (response.status !== 200) return;
        expect(response.body.Response).toEqual([]);
        expect(response.body.Pagination.older_url).toBeNull();
    });
});
