import {
    constants,
    sign,
    createPublicKey,
    verify
} from 'node:crypto';
import {Config} from "./config";

export const Signing = {
    signData: (config: Config, data: string): string => {
        const encodedData = Buffer.from(data, 'utf-8');
        const signer = sign('SHA256', encodedData, {
            key: config.signingKeys.privateKey(),
            padding: constants.RSA_PKCS1_PADDING,
        });
        const encodedSignature = signer.toString('base64');
        return encodedSignature;
    },

    verifyResponse: (config: Config, responseBody: string, signature: string): boolean => {
        try {
            const decodedSignature = Buffer.from(signature, 'base64');
            const verifier = verify(
                'SHA256',
                Buffer.from(responseBody, 'utf-8'),
                {
                    key: config.signingKeys.publicKey(),
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
}
