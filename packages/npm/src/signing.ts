import * as fs from 'node:fs';
import {
    generateKeyPairSync,
    constants,
    sign,
    createPrivateKey,
    createPublicKey,
    verify
} from 'node:crypto';
import {Config} from "./config";

export type Signing = {
    loadRsaKeyPair:() => Promise<[string, string]>
    signData:(data: string, privateKeyPem: string) => string
    verifyResponse: (responseBody: string, signature: string, serverPublicKeyPem: string) => Promise<boolean>
}
export const initSigning = (config: Config): Signing => ({
    loadRsaKeyPair: async () => {
        let privateKeyPem: string;
        let publicKeyPem: string;

        if (fs.existsSync(config.privateKeyFile) && fs.existsSync(config.publicKeyFile)) {
            privateKeyPem = fs.readFileSync(config.privateKeyFile, 'utf-8');
            publicKeyPem = fs.readFileSync(config.publicKeyFile, 'utf-8');
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

            fs.writeFileSync(config.privateKeyFile, privateKeyPem);
            fs.writeFileSync(config.publicKeyFile, publicKeyPem);
        }
        return [privateKeyPem, publicKeyPem] as const;
    },

    signData: (data, privateKeyPem: string) => {
        const privateKey = createPrivateKey(privateKeyPem);
        const encodedData = Buffer.from(data, 'utf-8');
        console.log(data);
        console.log(privateKeyPem);
        const signer = sign('SHA256', encodedData, {
            key: privateKey,
            padding: constants.RSA_PKCS1_PADDING,
        });
        const encodedSignature = signer.toString('base64');
        return encodedSignature;
    },

    verifyResponse: async (responseBody: string, signature: string, serverPublicKeyPem: string)=> {
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
})
