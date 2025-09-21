import * as crypto from 'node:crypto';

/**
 * Base class for configuration validation errors
 */
export abstract class ConfigValidationError extends Error {
    public readonly cause?: Error;
    
    constructor(message: string, cause?: Error) {
        super(message);
        this.name = this.constructor.name;
        this.cause = cause;
    }
}

/**
 * Error thrown when PEM format validation fails
 */
export class InvalidPemFormatError extends ConfigValidationError {}

/**
 * Error thrown when RSA key validation fails
 */
export class InvalidRsaKeyError extends ConfigValidationError {}

/**
 * Error thrown when private and public keys don't match
 */
export class KeyMismatchError extends ConfigValidationError {}

/**
 * Interface for RSA key pairs used in bunq API request signing.
 * 
 * Provides consistent access to both PEM string representations and parsed 
 * RSA key objects, ensuring they remain synchronized.
 * 
 * Available implementations:
 * - {@link SigningKeysFromPem} - Load from PEM strings (most common)
 * - {@link SigningKeysFromRsa} - Wrap existing RSA key objects
 */
export interface SigningKeys {
    privateKeyAsPem(): string;
    publicKeyAsPem(): string;
    privateKey(): crypto.KeyObject;
    publicKey(): crypto.KeyObject;
}

/**
 * SigningKeys implementation that loads from PEM string representations
 */
export class SigningKeysFromPem implements SigningKeys {
    private readonly privateKeyPem: string;
    private readonly publicKeyPem: string;
    private readonly privateKeyObj: crypto.KeyObject;
    private readonly publicKeyObj: crypto.KeyObject;

    constructor(privateKeyPem: string, publicKeyPem: string) {
        this.privateKeyPem = privateKeyPem;
        this.publicKeyPem = publicKeyPem;
        
        this.privateKeyObj = validateAndLoadPrivateKey(privateKeyPem);
        this.publicKeyObj = validateAndLoadPublicKey(publicKeyPem);
        
        validateKeyCompatibility(this.privateKeyObj, this.publicKeyObj);
    }

    privateKeyAsPem(): string {
        return this.privateKeyPem;
    }

    publicKeyAsPem(): string {
        return this.publicKeyPem;
    }

    privateKey(): crypto.KeyObject {
        return this.privateKeyObj;
    }

    publicKey(): crypto.KeyObject {
        return this.publicKeyObj;
    }
}

/**
 * SigningKeys implementation that wraps existing RSA key objects
 */
export class SigningKeysFromRsa implements SigningKeys {
    private readonly privateKeyObj: crypto.KeyObject;
    private readonly publicKeyObj: crypto.KeyObject;
    private readonly privateKeyPem: string;
    private readonly publicKeyPem: string;

    constructor(privateKey: crypto.KeyObject, publicKey: crypto.KeyObject) {
        this.privateKeyObj = privateKey;
        this.publicKeyObj = publicKey;
        
        validateKeyCompatibility(this.privateKeyObj, this.publicKeyObj);
        
        this.privateKeyPem = privateKey.export({
            type: 'pkcs8',
            format: 'pem'
        }).toString();
        
        this.publicKeyPem = publicKey.export({
            type: 'spki',
            format: 'pem'
        }).toString();
    }

    privateKeyAsPem(): string {
        return this.privateKeyPem;
    }

    publicKeyAsPem(): string {
        return this.publicKeyPem;
    }

    privateKey(): crypto.KeyObject {
        return this.privateKeyObj;
    }

    publicKey(): crypto.KeyObject {
        return this.publicKeyObj;
    }
}

function validateAndLoadPrivateKey(privateKeyPem: string): crypto.KeyObject {
    try {
        if (!privateKeyPem.includes('-----BEGIN PRIVATE KEY-----') ||
            !privateKeyPem.includes('-----END PRIVATE KEY-----')) {
            throw new InvalidPemFormatError('Private key must be in PKCS#8 PEM format');
        }

        const privateKey = crypto.createPrivateKey({
            key: privateKeyPem,
            format: 'pem'
        });

        if (privateKey.asymmetricKeyType !== 'rsa') {
            throw new InvalidRsaKeyError('Private key must be an RSA key');
        }

        return privateKey;
    } catch (error) {
        if (error instanceof ConfigValidationError) {
            throw error;
        }
        throw new InvalidRsaKeyError(`Failed to load private key: ${error}`, error as Error);
    }
}

function validateAndLoadPublicKey(publicKeyPem: string): crypto.KeyObject {
    try {
        if (!publicKeyPem.includes('-----BEGIN PUBLIC KEY-----') ||
            !publicKeyPem.includes('-----END PUBLIC KEY-----')) {
            throw new InvalidPemFormatError('Public key must be in X.509 PEM format');
        }

        const publicKey = crypto.createPublicKey({
            key: publicKeyPem,
            format: 'pem'
        });

        if (publicKey.asymmetricKeyType !== 'rsa') {
            throw new InvalidRsaKeyError('Public key must be an RSA key');
        }

        return publicKey;
    } catch (error) {
        if (error instanceof ConfigValidationError) {
            throw error;
        }
        throw new InvalidRsaKeyError(`Failed to load public key: ${error}`, error as Error);
    }
}

function validateKeyCompatibility(privateKey: crypto.KeyObject, publicKey: crypto.KeyObject): void {
    try {
        // Create a test signature to verify the keys are a matching pair
        const testData = 'test-signature-data';
        const signature = crypto.sign('sha256', Buffer.from(testData), privateKey);
        const isValid = crypto.verify('sha256', Buffer.from(testData), publicKey, signature);
        
        if (!isValid) {
            throw new KeyMismatchError('Private and public keys do not form a valid key pair');
        }
        
        // Additional check: verify key sizes are compatible (RSA public exponent check)
        const privateKeyDetails = privateKey.asymmetricKeyDetails as any;
        const publicKeyDetails = publicKey.asymmetricKeyDetails as any;
        
        if (privateKeyDetails?.publicExponent && publicKeyDetails?.publicExponent) {
            if (privateKeyDetails.publicExponent.toString() !== publicKeyDetails.publicExponent.toString()) {
                throw new KeyMismatchError('Private and public keys have mismatched exponents');
            }
            
            // Standard RSA public exponent check
            const expectedExponent = BigInt(65537);
            if (privateKeyDetails.publicExponent !== expectedExponent) {
                throw new InvalidRsaKeyError(`Public key has unexpected exponent. Expected 65537, got ${privateKeyDetails.publicExponent}`);
            }
        }
    } catch (error) {
        if (error instanceof ConfigValidationError) {
            throw error;
        }
        throw new KeyMismatchError(`Failed to validate key compatibility: ${error}`);
    }
}