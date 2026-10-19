import {createSign, generateKeyPairSync} from 'node:crypto';
import {ServerResponse} from 'node:http';

/** Stands in for bunq's server key: local test servers sign their responses with it. */
const {privateKey, publicKey} = generateKeyPairSync('rsa', {
    modulusLength: 2048,
    privateKeyEncoding: {type: 'pkcs8', format: 'pem'},
    publicKeyEncoding: {type: 'spki', format: 'pem'},
});

export const serverPublicKey = publicKey;

export const signBody = (body: string | Uint8Array): string => createSign('SHA256').update(body).sign(privateKey, 'base64');

/** Ends the response with [body] and an X-Bunq-Server-Signature header (none when signature is null). */
export function respond(res: ServerResponse, status: number, body: string, signature: string | null = signBody(body)) {
    res.statusCode = status;
    if (signature !== null) res.setHeader('X-Bunq-Server-Signature', signature);
    res.end(body);
}
