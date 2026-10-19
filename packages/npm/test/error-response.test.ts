import {afterEach, describe, expect, test} from 'vitest';
import {createServer, Server} from 'node:http';
import {AddressInfo} from 'node:net';
import {generateKeyPairSync} from 'node:crypto';
import {createConfig} from "../src/config";
import {respond, serverPublicKey} from "./server-key";
import {Context} from "../src/context";
import {bunqClient} from "../src/transportation";
import {ReadUser} from "../src/gen/endpoint/ReadUser";
import {BunqApiError, serialization} from "../src/wirespec";

describe('error responses', () => {
    let server: Server;

    afterEach(() => new Promise(resolve => server.close(resolve)));

    async function readUserAnswering(status: number, body: string) {
        server = createServer((req, res) => {
            respond(res, status, body);
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
        return bunqClient(context).readUser({itemId: 1});
    }

    test('a 400 error body without Response envelope is a typed Response400', async () => {
        const response = await readUserAnswering(400, '{"Error":[{"error_description":"Missing required field \\"currency\\"."}]}');

        expect(response.status).toBe(400);
        expect(response.body).toEqual({Error: [{error_description: 'Missing required field "currency".'}]});
    });

    test('a body without Response or Error is rejected', () => {
        const raw = {statusCode: 200, headers: {}, body: new TextEncoder().encode('{"unexpected":true}')};

        expect(() => ReadUser.fromRawResponse(serialization, raw)).toThrow('neither Response nor Error');
    });

    test.each([403, 404, 500])('a %i throws with the status and body', async status => {
        const body = `{"Error":[{"error_description":"nope ${status}"}]}`;

        await expect(readUserAnswering(status, body)).rejects.toMatchObject({status, body});
    });

    test('an HTML 500 throws with the HTML as body', async () => {
        await expect(readUserAnswering(500, '<html>Internal Server Error</html>'))
            .rejects.toMatchObject({status: 500, body: '<html>Internal Server Error</html>'});
    });

    test('a 400 that is not JSON throws', async () => {
        await expect(readUserAnswering(400, '<html>Bad Request</html>')).rejects.toBeInstanceOf(BunqApiError);
    });

    test('a 200 without Response throws with the status and body', async () => {
        await expect(readUserAnswering(200, '{"unexpected":true}'))
            .rejects.toMatchObject({status: 200, body: '{"unexpected":true}'});
    });

    test('a 400 without Error throws with the status and body', async () => {
        await expect(readUserAnswering(400, '{"message":"Bad Request"}'))
            .rejects.toMatchObject({status: 400, body: '{"message":"Bad Request"}'});
    });

    test('a non-object JSON 200 throws', async () => {
        await expect(readUserAnswering(200, '[]')).rejects.toMatchObject({status: 200, body: '[]'});
    });

    test('the message truncates the body but the body field keeps it whole', () => {
        const error = new BunqApiError(502, 'x'.repeat(2000));

        expect(error.message.length).toBeLessThan(600);
        expect(error.body).toHaveLength(2000);
    });

    test('a 200 is returned as is', async () => {
        const response = await readUserAnswering(200, '{"Response":[{"UserPerson":{"id":1}}]}');

        expect(response.status).toBe(200);
    });
});
