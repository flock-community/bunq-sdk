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

    /** Verifies bunq's `X-Bunq-Server-Signature`: SHA256withRSA over the raw response body bytes. */
    verifyResponse: (serverPublicKeyPem: string, responseBody: Uint8Array, signature: string | undefined): boolean => {
        try {
            if (!signature) return false;
            return verify(
                'SHA256',
                responseBody,
                {
                    key: createPublicKey(serverPublicKeyPem),
                    padding: constants.RSA_PKCS1_PADDING,
                },
                Buffer.from(signature, 'base64')
            );
        } catch (e: any) {
            console.error(`[ERROR] Signature verification failed: ${e}`);
            return false;
        }
    }
}
