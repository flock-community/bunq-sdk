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

export type KeyType = 'PRIVATE' | 'PUBLIC' | 'BOTH';
export type ValidationStage = 'PEM_PARSING' | 'RSA_VALIDATION' | 'COMPATIBILITY_CHECK';

const KEY_TYPE_LABELS: Record<KeyType, string> = {
    PRIVATE: 'Private key',
    PUBLIC: 'Public key',
    BOTH: 'Private and public key',
};

const STAGE_LABELS: Record<ValidationStage, string> = {
    PEM_PARSING: 'PEM parsing',
    RSA_VALIDATION: 'RSA validation',
    COMPATIBILITY_CHECK: 'compatibility check',
};

/**
 * Signing key validation failure. The message reads
 * "<key> validation failed during <stage>: <detail>".
 */
export abstract class SigningKeyValidationError extends ConfigValidationError {
    constructor(
        detail: string,
        public readonly keyType: KeyType,
        public readonly stage: ValidationStage,
        cause?: Error,
    ) {
        super(`${KEY_TYPE_LABELS[keyType]} validation failed during ${STAGE_LABELS[stage]}: ${detail}`, cause);
    }
}

/**
 * Error thrown when PEM format validation fails
 */
export class InvalidPemFormatError extends SigningKeyValidationError {
    constructor(detail: string, keyType: KeyType, cause?: Error) {
        super(detail, keyType, 'PEM_PARSING', cause);
    }
}

/**
 * Error thrown when RSA key validation fails
 */
export class InvalidRsaKeyError extends SigningKeyValidationError {
    constructor(detail: string, keyType: KeyType, cause?: Error) {
        super(detail, keyType, 'RSA_VALIDATION', cause);
    }
}

/**
 * Error thrown when private and public keys don't match
 */
export class KeyMismatchError extends SigningKeyValidationError {
    constructor(detail: string) {
        super(detail, 'BOTH', 'COMPATIBILITY_CHECK');
    }
}

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
    readonly #privateKeyPem: string;
    private readonly publicKeyPem: string;
    private readonly privateKeyObj: crypto.KeyObject;
    private readonly publicKeyObj: crypto.KeyObject;

    constructor(privateKeyPem: string, publicKeyPem: string) {
        this.#privateKeyPem = privateKeyPem;
        this.publicKeyPem = publicKeyPem;
        
        this.privateKeyObj = validateAndLoadPrivateKey(privateKeyPem);
        this.publicKeyObj = validateAndLoadPublicKey(publicKeyPem);
        
        validateKeyCompatibility(this.privateKeyObj, this.publicKeyObj);
    }

    privateKeyAsPem(): string {
        return this.#privateKeyPem;
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
    readonly #privateKeyPem: string;
    private readonly publicKeyPem: string;

    constructor(privateKey: crypto.KeyObject, publicKey: crypto.KeyObject) {
        this.privateKeyObj = privateKey;
        this.publicKeyObj = publicKey;
        
        validateKeyCompatibility(this.privateKeyObj, this.publicKeyObj);
        
        this.#privateKeyPem = privateKey.export({
            type: 'pkcs8',
            format: 'pem'
        }).toString();
        
        this.publicKeyPem = publicKey.export({
            type: 'spki',
            format: 'pem'
        }).toString();
    }

    privateKeyAsPem(): string {
        return this.#privateKeyPem;
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

const PKCS8_FIX =
    'openssl pkcs8 -topk8 -inform PEM -outform PEM -nocrypt -in private_key.pem -out private_key_pkcs8.pem';
const PUBLIC_FROM_PRIVATE_FIX = 'openssl rsa -in private_key_pkcs8.pem -pubout -out public_key.pem';

function validateAndLoadPrivateKey(privateKeyPem: string): crypto.KeyObject {
    const der = readPemBody(privateKeyPem, 'PRIVATE KEY', 'PRIVATE');
    return loadRsaKey(
        () => crypto.createPrivateKey({ key: der, format: 'der', type: 'pkcs8' }),
        'PRIVATE',
        'Generate one with: openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048',
    );
}

function validateAndLoadPublicKey(publicKeyPem: string): crypto.KeyObject {
    const der = readPemBody(publicKeyPem, 'PUBLIC KEY', 'PUBLIC');
    return loadRsaKey(
        () => crypto.createPublicKey({ key: der, format: 'der', type: 'spki' }),
        'PUBLIC',
        `Derive it with: ${PUBLIC_FROM_PRIVATE_FIX}`,
    );
}

function loadRsaKey(load: () => crypto.KeyObject, keyType: KeyType, hint: string): crypto.KeyObject {
    const notRsa = (reason: string, cause?: Error) =>
        new InvalidRsaKeyError(
            `not a valid RSA key (${reason}). The key may be truncated or corrupted, or not an RSA key ` +
            `(only RSA keys are supported). ${hint}`,
            keyType,
            cause,
        );
    let key: crypto.KeyObject;
    try {
        key = load();
    } catch (error) {
        throw notRsa((error as Error).message, error as Error);
    }
    if (key.asymmetricKeyType !== 'rsa') {
        throw notRsa(`key type is '${key.asymmetricKeyType}'`);
    }
    return key;
}

const BASE64 = /^[A-Za-z0-9+/]*={0,2}$/;

function decodePemBody(body: string[]): { headers: string[]; content: Buffer } {
    const headers = body.filter((line) => line.includes(':'));
    const base64 = body.filter((line) => !line.includes(':')).join('');
    if (!BASE64.test(base64) || base64.length % 4 !== 0) {
        throw new Error('invalid base64');
    }
    return { headers, content: Buffer.from(base64, 'base64') };
}

function readPemBody(pem: string, label: string, keyType: KeyType): Buffer {
    const invalid = (detail: string, cause?: Error) => new InvalidPemFormatError(detail, keyType, cause);

    if (pem.includes('\\n')) {
        throw invalid('the PEM contains literal \\n sequences; replace them with real newlines');
    }
    const lines = pem.split(/\r\n|\r|\n/).map((line) => line.trim()).filter((line) => line.length > 0);
    if (lines.length < 2) {
        throw invalid('the PEM has no line breaks; put the BEGIN line, the base64 body and the END line on separate lines');
    }
    const beginIndex = lines.findIndex((line) => /^-----BEGIN .+-----$/.test(line));
    if (beginIndex < 0) {
        throw invalid('no PEM block could be read; check that the BEGIN line is present and the line breaks are real newlines');
    }
    const type = lines[beginIndex].slice('-----BEGIN '.length, -'-----'.length);
    const endIndex = lines.indexOf(`-----END ${type}-----`, beginIndex + 1);
    if (endIndex < 0) {
        throw invalid(`the '-----END ${label}-----' line is missing, the PEM looks truncated`);
    }

    let block: { type: string; headers: string[]; content: Buffer };
    try {
        block = { type, ...decodePemBody(lines.slice(beginIndex + 1, endIndex)) };
    } catch (error) {
        throw invalid(
            `the body is not valid base64 or is malformed (${(error as Error).message}). Re-export the key without modifying it.`,
            error as Error,
        );
    }

    const encrypted = block.type === 'ENCRYPTED PRIVATE KEY' ||
        block.headers.some((header) => header.startsWith('Proc-Type:') && header.includes('ENCRYPTED'));
    const expectsPrivate = keyType === 'PRIVATE';
    if (block.type === label && !encrypted) {
        return block.content;
    }
    if (encrypted && expectsPrivate) {
        throw invalid(
            'the key is encrypted, which is not supported. Decrypt it first (the command asks for the passphrase): ' +
            'openssl pkcs8 -topk8 -nocrypt -in encrypted_key.pem -out private_key_pkcs8.pem');
    }
    if (block.type === 'RSA PRIVATE KEY' && expectsPrivate) {
        throw invalid(`the key is in PKCS#1 format but PKCS#8 ('-----BEGIN PRIVATE KEY-----') is required. Convert it with: ${PKCS8_FIX}`);
    }
    if (block.type === 'RSA PUBLIC KEY' && !expectsPrivate) {
        throw invalid(
            "the key is in PKCS#1 format but X.509 ('-----BEGIN PUBLIC KEY-----') is required. Convert it with: " +
            'openssl rsa -RSAPublicKey_in -in public_key.pem -pubout -out public_key_spki.pem');
    }
    if (expectsPrivate && block.type.endsWith('PUBLIC KEY')) {
        throw invalid('this is a public key, a private key is expected. The keys may be swapped.');
    }
    if (!expectsPrivate && block.type.endsWith('PRIVATE KEY')) {
        throw invalid(
            'this is a private key, a public key is expected. The keys may be swapped. ' +
            `Derive the public key with: ${PUBLIC_FROM_PRIVATE_FIX}`);
    }
    throw invalid(`the first PEM block is '${block.type}' but '${label}' is expected`);
}

function validateKeyCompatibility(privateKey: crypto.KeyObject, publicKey: crypto.KeyObject): void {
    const exponent = publicKey.asymmetricKeyDetails?.publicExponent;
    if (exponent !== BigInt(65537)) {
        throw new InvalidRsaKeyError(`unexpected public exponent. Expected 65537, got ${exponent}`, 'PUBLIC');
    }
    if (privateKey.export({ format: 'jwk' }).n !== publicKey.export({ format: 'jwk' }).n) {
        throw new KeyMismatchError(`the keys do not form a pair (the moduli differ). Derive the public key with: ${PUBLIC_FROM_PRIVATE_FIX}`);
    }
}
