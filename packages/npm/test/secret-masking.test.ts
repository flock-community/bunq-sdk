import {expect, test} from 'vitest';
import {generateKeyPairSync} from 'node:crypto';
import {createConfig, describeConfig} from "../src/config";
import {Context, describeContext} from "../src/context";

test('describeContext masks secrets and keeps non-secret fields', () => {
    const {privateKey, publicKey} = generateKeyPairSync('rsa', {
        modulusLength: 2048,
        privateKeyEncoding: {type: 'pkcs8', format: 'pem'},
        publicKeyEncoding: {type: 'spki', format: 'pem'},
    });
    const config = createConfig({baseUrl: 'http://localhost/', pinnedKey: ''}, 'my-service', 'secret-api-key', privateKey, publicKey);
    const context: Context = {
        serverPublicKey: 'server-key', deviceId: 1, sessionId: 2, sessionToken: 'secret-session', userId: 3,
        sessionExpiryTime: new Date(0), installationToken: 'secret-install', config,
    };

    for (const text of [describeContext(context), describeConfig(config)]) {
        for (const secret of ['secret-api-key', 'secret-session', 'secret-install', privateKey.split('\n')[1]]) {
            expect(text).not.toContain(secret);
        }
        expect(text).toContain('my-service');
    }
    expect(describeContext(context)).toContain('"userId":3');
    expect(JSON.stringify(config)).not.toContain(privateKey.split('\n')[1]);
});
