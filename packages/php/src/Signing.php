<?php

declare(strict_types=1);

namespace Bunq\Sdk;

/**
 * bunq signs with SHA256withRSA (PKCS#1 v1.5): requests in `X-Bunq-Client-Signature`, responses in `X-Bunq-Server-Signature`.
 */
final class Signing
{
    /** The base64 signature of the request body, made with the config's private key. */
    public static function signData(Config $config, string $data): string
    {
        \openssl_sign($data, $signature, $config->signingKeys->privateKey(), \OPENSSL_ALGO_SHA256)
            ?: throw new \RuntimeException('Cannot sign the request: ' . \openssl_error_string());
        return \base64_encode($signature);
    }

    /** Whether the signature is bunq's signature over the raw response body; false for a missing or malformed signature. */
    public static function verifyResponse(string $serverPublicKeyPem, string $responseBody, ?string $signature): bool
    {
        try {
            $decoded = $signature === null ? false : \base64_decode($signature, true);
            return $decoded !== false && $decoded !== ''
                && \openssl_verify($responseBody, $decoded, SigningKeys::loadPublicKey($serverPublicKeyPem), \OPENSSL_ALGO_SHA256) === 1;
        } catch (InvalidConfigError $e) {
            \error_log("bunq - signature verification failed: {$e->getMessage()}");
            return false;
        }
    }
}
