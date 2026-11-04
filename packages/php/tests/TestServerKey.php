<?php

declare(strict_types=1);

namespace Bunq\Sdk\Tests;

use Bunq\Api\Wirespec;
use Bunq\Sdk\BunqServer;
use Bunq\Sdk\Config;
use Bunq\Sdk\Context;
use Bunq\Sdk\SigningKeys;

/**
 * Stands in for bunq's server key, so tests can answer with signed responses.
 */
final class TestServerKey
{
    private static ?SigningKeys $server = null;
    private static ?SigningKeys $client = null;

    public static function keys(): SigningKeys
    {
        return self::$server ??= SigningKeys::generate();
    }

    public static function publicKey(): string
    {
        return self::keys()->publicKeyAsPem();
    }

    public static function sign(string $body): string
    {
        \openssl_sign($body, $signature, self::keys()->privateKey(), \OPENSSL_ALGO_SHA256);
        return \base64_encode($signature);
    }

    /** A response with a valid `X-Bunq-Server-Signature` by default, none when $signature is null. */
    public static function response(int $status, string $body, ?string $signature = 'valid'): Wirespec\RawResponse
    {
        $headers = $signature === null ? [] : ['X-Bunq-Server-Signature' => [$signature === 'valid' ? self::sign($body) : $signature]];
        return new Wirespec\RawResponse(statusCode: $status, headers: $headers, body: $body);
    }

    public static function config(string $baseUrl = 'https://example.invalid/v1/', ?string $userAgent = null): Config
    {
        return new Config(new BunqServer($baseUrl, ''), 'PhpTest', 'api-key', self::$client ??= SigningKeys::generate(), $userAgent);
    }

    public static function context(string $sessionToken = 'session-1', string $expiresIn = '+1 hour'): Context
    {
        return new Context(
            serverPublicKey: self::publicKey(),
            deviceId: 1,
            sessionId: 2,
            sessionToken: $sessionToken,
            userId: 3,
            sessionExpiryTime: new \DateTimeImmutable($expiresIn),
            installationToken: 'installation',
            config: self::config(),
        );
    }
}
