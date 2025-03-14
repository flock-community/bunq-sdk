import * as fs from 'node:fs';
import {
    generateKeyPairSync,
    constants,
    sign,
    createPrivateKey,
    createPublicKey,
    verify
} from 'node:crypto';

const privateKeyFile = 'private_key.pem';
const publicKeyFile = 'public_key.pem';

export async function loadRsaKeyPair(): Promise<[string, string]> {
    let privateKeyPem: string;
    let publicKeyPem: string;

    if (fs.existsSync(privateKeyFile) && fs.existsSync(publicKeyFile)) {
        privateKeyPem = fs.readFileSync(privateKeyFile, 'utf-8');
        publicKeyPem = fs.readFileSync(publicKeyFile, 'utf-8');
    } else {
        const { privateKey, publicKey } = generateKeyPairSync('rsa', {
            modulusLength: 2048
        });

        privateKeyPem = privateKey.export({
            type: 'pkcs8',
            format: 'pem',
        }).toString();

       publicKeyPem = publicKey.export({
            type: 'spki',
            format: 'pem',
        }).toString();

        fs.writeFileSync(privateKeyFile, privateKeyPem);
        fs.writeFileSync(publicKeyFile, publicKeyPem);
    }
    return [privateKeyPem, publicKeyPem];
}

export function signData(data: string, privateKeyPem: string): string {
    const privateKey = createPrivateKey(privateKeyPem);
    const encodedData = Buffer.from(data, 'utf-8');
    const signer = sign('SHA256', encodedData, {
        key: privateKey,
        padding: constants.RSA_PKCS1_PADDING,
    });
    const encodedSignature = signer.toString('base64');
    return encodedSignature;
}

export async function verifyResponse(responseBody: string, signature: string, serverPublicKeyPem: string): Promise<boolean> {
    try {
        const publicKey = createPublicKey(serverPublicKeyPem)
        const decodedSignature = Buffer.from(signature, 'base64');
        const verifier = verify(
            'SHA256',
            Buffer.from(responseBody, 'utf-8'),
            {
                key: publicKey,
                padding: constants.RSA_PKCS1_PADDING,
            },
            decodedSignature
        );
        return verifier;
    } catch (e: any) {
        console.error(`[ERROR] Signature verification failed: ${e}`);
        return false;
    }
}