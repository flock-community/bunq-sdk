import { BunqServer } from './bunq-server';
import { SigningKeys, SigningKeysFromPem } from './signing-keys';

/**
 * Error thrown when basic config validation fails
 */
export class InvalidConfigError extends Error {
    public readonly cause?: Error;
    
    constructor(message: string, cause?: Error) {
        super(message);
        this.name = this.constructor.name;
        this.cause = cause;
    }
}

/**
 * Configuration type for bunq API client containing all necessary settings and credentials
 * for establishing and managing API connections.
 * 
 * All parameters are validated to ensure proper format and compatibility.
 */
export interface Config {
    /** The bunq API server configuration including base URL and pinned key */
    readonly bunqServer: BunqServer;
    /** Name of the service/application using the bunq API */
    readonly serviceName: string;
    /** API key for authentication with bunq servers */
    readonly apiKey: string;
    /** Key pair for server-side request signing */
    readonly signingKeys: SigningKeys;
    /** Custom user agent string for API requests */
    readonly userAgent?: string;
    /** Cache control header value for API requests */
    readonly cacheControl?: string;
    /** Preferred language for API responses */
    readonly language?: string;
    /** Geographic region for API requests */
    readonly region?: string;
    /** Custom client request ID for tracking API calls */
    readonly clientRequestId?: string;
    /** Geolocation information for API requests */
    readonly geolocation?: string;
}

/**
 * Creates a configuration object from basic parameters.
 * The configuration is validated during construction.
 */
export function createConfig(
    bunqServer: BunqServer,
    serviceName: string,
    apiKey: string,
    privateKeyPem: string,
    publicKeyPem: string,
    options?: {
        userAgent?: string;
        cacheControl?: string;
        language?: string;
        region?: string;
        clientRequestId?: string;
        geolocation?: string;
    }
): Config {
    validateBasicParameters(serviceName, apiKey);
    
    const signingKeys = new SigningKeysFromPem(privateKeyPem, publicKeyPem);
    
    return {
        bunqServer,
        serviceName,
        apiKey,
        signingKeys,
        userAgent: options?.userAgent,
        cacheControl: options?.cacheControl,
        language: options?.language,
        region: options?.region,
        clientRequestId: options?.clientRequestId,
        geolocation: options?.geolocation,
    };
}

function validateBasicParameters(serviceName: string, apiKey: string): void {
    if (!serviceName?.trim()) {
        throw new InvalidConfigError('Service name cannot be blank');
    }
    if (!apiKey?.trim()) {
        throw new InvalidConfigError('API key cannot be blank');
    }
}