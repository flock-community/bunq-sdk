import { describe, expect, test } from 'vitest';
import * as crypto from 'node:crypto';
import {
    InvalidPemFormatError,
    InvalidRsaKeyError,
    KeyMismatchError,
    SigningKeyValidationError,
    SigningKeysFromPem,
    type KeyType,
    type ValidationStage,
} from '../src/signing-keys';

function generate() {
    const pair = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
    return {
        privatePem: pair.privateKey.export({ type: 'pkcs8', format: 'pem' }).toString(),
        publicPem: pair.publicKey.export({ type: 'spki', format: 'pem' }).toString(),
        pkcs1PrivatePem: pair.privateKey.export({ type: 'pkcs1', format: 'pem' }).toString(),
        pkcs1PublicPem: pair.publicKey.export({ type: 'pkcs1', format: 'pem' }).toString(),
    };
}

const valid = generate();

function pem(type: string, der: Buffer): string {
    const body = der.toString('base64').match(/.{1,64}/g)!.join('\n');
    return `-----BEGIN ${type}-----\n${body}\n-----END ${type}-----\n`;
}

function expectFailure(
    errorClass: new (...args: any[]) => SigningKeyValidationError,
    keyType: KeyType,
    stage: ValidationStage,
    phrase: string,
    block: () => void,
) {
    let caught: unknown;
    try {
        block();
    } catch (error) {
        caught = error;
    }
    expect(caught).toBeInstanceOf(errorClass);
    const e = caught as SigningKeyValidationError;
    expect(e.keyType).toBe(keyType);
    expect(e.stage).toBe(stage);
    expect(e.message).toContain(phrase);
    console.log(`MESSAGE[${phrase}]: ${e.message}`);
}

describe('signing key validation', () => {
    test('PKCS1 private key gets openssl conversion command', () => {
        const pkcs1 = valid.pkcs1PrivatePem;
        expectFailure(InvalidPemFormatError, 'PRIVATE', 'PEM_PARSING',
            'Private key validation failed during PEM parsing: the key is in PKCS#1 format',
            () => new SigningKeysFromPem(pkcs1, valid.publicPem));
        expectFailure(InvalidPemFormatError, 'PRIVATE', 'PEM_PARSING',
            'openssl pkcs8 -topk8 -inform PEM -outform PEM -nocrypt -in private_key.pem -out private_key_pkcs8.pem',
            () => new SigningKeysFromPem(pkcs1, valid.publicPem));
    });

    test('encrypted private key is rejected', () => {
        const encrypted = pem('ENCRYPTED PRIVATE KEY', Buffer.from('0123456789'));
        expectFailure(InvalidPemFormatError, 'PRIVATE', 'PEM_PARSING', 'the command asks for the passphrase',
            () => new SigningKeysFromPem(encrypted, valid.publicPem));
    });

    test('truncated PEM reports missing END line', () => {
        const truncated = valid.privatePem.split('-----END')[0];
        expectFailure(InvalidPemFormatError, 'PRIVATE', 'PEM_PARSING', 'looks truncated',
            () => new SigningKeysFromPem(truncated, valid.publicPem));
    });

    test('invalid base64 body is rejected', () => {
        const bad = '-----BEGIN PUBLIC KEY-----\n!!!not base64!!!\n-----END PUBLIC KEY-----\n';
        expectFailure(InvalidPemFormatError, 'PUBLIC', 'PEM_PARSING', 'not valid base64',
            () => new SigningKeysFromPem(valid.privatePem, bad));
    });

    test('EC private key is rejected as non RSA', () => {
        const ec = crypto.generateKeyPairSync('ec', { namedCurve: 'prime256v1' })
            .privateKey.export({ type: 'pkcs8', format: 'pem' }).toString();
        expectFailure(InvalidRsaKeyError, 'PRIVATE', 'RSA_VALIDATION',
            'Private key validation failed during RSA validation',
            () => new SigningKeysFromPem(ec, valid.publicPem));
    });

    test('mismatched key pair is reported for both keys', () => {
        const other = generate();
        expectFailure(KeyMismatchError, 'BOTH', 'COMPATIBILITY_CHECK',
            'Private and public key validation failed during compatibility check',
            () => new SigningKeysFromPem(valid.privatePem, other.publicPem));
    });

    test('literal backslash n is detected', () => {
        const envVar = valid.privatePem.trim().replace(/\n/g, '\\n');
        expectFailure(InvalidPemFormatError, 'PRIVATE', 'PEM_PARSING', 'literal \\n sequences',
            () => new SigningKeysFromPem(envVar, valid.publicPem));
    });

    test('single line PEM is detected', () => {
        const oneLine = valid.publicPem.trim().replace(/\n/g, ' ');
        expectFailure(InvalidPemFormatError, 'PUBLIC', 'PEM_PARSING', 'no line breaks',
            () => new SigningKeysFromPem(valid.privatePem, oneLine));
    });

    test('certificate before the key is reported as wrong block', () => {
        const cert = pem('CERTIFICATE', Buffer.from([1, 2, 3])) + valid.publicPem;
        expectFailure(InvalidPemFormatError, 'PUBLIC', 'PEM_PARSING', "the first PEM block is 'CERTIFICATE'",
            () => new SigningKeysFromPem(valid.privatePem, cert));
    });

    test('PKCS1 public key gets conversion command', () => {
        expectFailure(InvalidPemFormatError, 'PUBLIC', 'PEM_PARSING',
            'openssl rsa -RSAPublicKey_in -in public_key.pem -pubout -out public_key_spki.pem',
            () => new SigningKeysFromPem(valid.privatePem, valid.pkcs1PublicPem));
    });

    test('public key passed as private key', () => {
        expectFailure(InvalidPemFormatError, 'PRIVATE', 'PEM_PARSING', 'may be swapped',
            () => new SigningKeysFromPem(valid.publicPem, valid.publicPem));
    });

    test('private key passed as public key', () => {
        expectFailure(InvalidPemFormatError, 'PUBLIC', 'PEM_PARSING', 'may be swapped',
            () => new SigningKeysFromPem(valid.privatePem, valid.privatePem));
    });

    test('CR only line endings load', () => {
        expect(() => new SigningKeysFromPem(valid.privatePem.replace(/\n/g, '\r'), valid.publicPem)).not.toThrow();
    });

    test('trailing spaces load', () => {
        const spaced = valid.privatePem.split('\n').map((l) => `${l}   `).join('\n');
        expect(() => new SigningKeysFromPem(spaced, valid.publicPem)).not.toThrow();
    });

    test('indented PEM loads', () => {
        const indented = valid.publicPem.split('\n').map((l) => `    ${l}`).join('\n');
        expect(() => new SigningKeysFromPem(valid.privatePem, indented)).not.toThrow();
    });

    test('concatenated private and public PEM uses the first block', () => {
        expect(() => new SigningKeysFromPem(valid.privatePem + valid.publicPem, valid.publicPem)).not.toThrow();
    });

    test('dropped body line mentions truncated or corrupted', () => {
        const lines = valid.privatePem.split('\n');
        lines.splice(2, 1);
        expectFailure(InvalidRsaKeyError, 'PRIVATE', 'RSA_VALIDATION', 'may be truncated or corrupted',
            () => new SigningKeysFromPem(lines.join('\n'), valid.publicPem));
    });
});
