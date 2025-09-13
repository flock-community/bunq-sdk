import * as crypto from 'crypto';

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
 * Error thrown when basic config validation fails
 */
export class InvalidConfigError extends ConfigValidationError {}

/**
 * Configuration type for bunq API client containing all necessary settings and credentials
 * for establishing and managing API connections.
 * 
 * All parameters are validated to ensure proper format and compatibility.
 */
export type Config = {
    serverName: string;
    apiKey: string;
    privateKeyPem: string;
    publicKeyPem: string;
    userAgent?: string;
    cacheControl?: string;
    language?: string;
    region?: string;
    clientRequestId?: string;
    geolocation?: string;
};

/**
 * Validated configuration with parsed RSA keys for internal use
 */
export type ValidatedConfig = Config & {
    privateKey: crypto.KeyObject;
    publicKey: crypto.KeyObject;
};

/**
 * Creates and validates a configuration object.
 * Throws ConfigValidationError if validation fails.
 */
export const createConfig = (config: Config): ValidatedConfig => {
    validateBasicParameters(config);
    
    const privateKey = validateAndLoadPrivateKey(config.privateKeyPem);
    const publicKey = validateAndLoadPublicKey(config.publicKeyPem);
    
    validateKeyCompatibility(privateKey, publicKey);
    
    return {
        ...config,
        privateKey,
        publicKey
    };
};

/**
 * Gets the public key as a PEM string for API usage.
 */
export const getPublicKeyAsString = (config: Config): string => {
    return config.publicKeyPem;
};

function validateBasicParameters(config: Config): void {
    if (!config.serverName?.trim()) {
        throw new InvalidConfigError('Server name cannot be blank');
    }
    if (!config.apiKey?.trim()) {
        throw new InvalidConfigError('API key cannot be blank');
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
        
        // Additional check: verify key sizes are compatible
        const privateKeyDetails = privateKey.asymmetricKeyDetails as any;
        const publicKeyDetails = publicKey.asymmetricKeyDetails as any;
        
        if (privateKeyDetails?.mgf && publicKeyDetails?.mgf) {
            if (privateKeyDetails.keySize !== publicKeyDetails.keySize) {
                throw new KeyMismatchError('Private and public keys have different key sizes');
            }
        }
    } catch (error) {
        if (error instanceof ConfigValidationError) {
            throw error;
        }
        throw new KeyMismatchError(`Failed to validate key compatibility: ${error}`);
    }
}

// Legacy support - deprecated
/**
 * @deprecated Use createConfig instead
 */
export const initConfig: (config: Omit<Config, 'privateKeyPem' | 'publicKeyPem'> & {
    privateKeyFile?: string;
    publicKeyFile?: string;
}) => Config = (config) => {
    throw new Error('File-based configuration is deprecated. Use PEM strings with createConfig instead.');
};