<?php

declare(strict_types=1);

namespace Bunq\Sdk\Tests;

use Bunq\Sdk\BunqServer;
use Bunq\Sdk\Config;
use Bunq\Sdk\InvalidConfigError;
use Bunq\Sdk\SigningKeys;
use Bunq\Sdk\SigningKeyValidationError;
use PHPUnit\Framework\TestCase;

final class ConfigTest extends TestCase
{
    public function testDumpMasksTheSecretsAndKeepsTheOtherFields(): void
    {
        $context = TestServerKey::context('session-secret');

        $dump = \print_r($context, true);

        self::assertStringNotContainsString('session-secret', $dump);
        self::assertStringNotContainsString('api-key', $dump);
        self::assertStringNotContainsString('PRIVATE KEY', $dump);
        self::assertStringContainsString('PhpTest', $dump);
        self::assertStringContainsString('***', $dump);
    }

    public function testBlankServiceNameOrApiKeyIsRejected(): void
    {
        $keys = SigningKeys::generate();
        foreach ([[' ', 'key', 'Service name cannot be blank'], ['PhpTest', '', 'API key cannot be blank']] as [$service, $apiKey, $message]) {
            try {
                new Config(BunqServer::sandbox(), $service, $apiKey, $keys);
                self::fail("Expected: $message");
            } catch (InvalidConfigError $error) {
                self::assertSame($message, $error->getMessage());
            }
        }
    }

    public function testNonPositiveTimeoutIsRejected(): void
    {
        $this->expectExceptionMessage('Request timeout must be positive');
        new Config(BunqServer::sandbox(), 'PhpTest', 'key', SigningKeys::generate(), requestTimeout: 0.0);
    }

    public function testGeneratedKeysCanBeLoadedFromTheirPem(): void
    {
        $keys = SigningKeys::generate();

        $loaded = new SigningKeys($keys->privateKeyAsPem(), $keys->publicKeyAsPem());

        self::assertSame($keys->publicKeyAsPem(), $loaded->publicKeyAsPem());
    }

    public function testPkcs1PrivateKeyGetsTheConversionCommand(): void
    {
        $keys = SigningKeys::generate();
        $pkcs1 = \str_replace('PRIVATE KEY', 'RSA PRIVATE KEY', $keys->privateKeyAsPem());

        $this->expectValidationError("Private key validation failed during PEM parsing: the key is in PKCS#1 format but PKCS#8 ('-----BEGIN PRIVATE KEY-----') is required. Convert it with: openssl pkcs8");
        new SigningKeys($pkcs1, $keys->publicKeyAsPem());
    }

    public function testSwappedKeysAreReported(): void
    {
        $keys = SigningKeys::generate();

        $this->expectValidationError('Private key validation failed during PEM parsing: this is a public key, a private key is expected.');
        new SigningKeys($keys->publicKeyAsPem(), $keys->privateKeyAsPem());
    }

    public function testMismatchedKeyPairIsReportedForBothKeys(): void
    {
        $this->expectValidationError('Private and public key validation failed during compatibility check: the keys do not form a pair');
        new SigningKeys(SigningKeys::generate()->privateKeyAsPem(), SigningKeys::generate()->publicKeyAsPem());
    }

    public function testLiteralBackslashNIsDetected(): void
    {
        $keys = SigningKeys::generate();

        $this->expectValidationError('Private key validation failed during PEM parsing: the PEM contains literal \n sequences');
        new SigningKeys(\str_replace("\n", '\n', $keys->privateKeyAsPem()), $keys->publicKeyAsPem());
    }

    public function testTruncatedPemReportsTheMissingEndLine(): void
    {
        $keys = SigningKeys::generate();
        $truncated = \substr($keys->privateKeyAsPem(), 0, \strpos($keys->privateKeyAsPem(), '-----END'));

        $this->expectValidationError("Private key validation failed during PEM parsing: the '-----END PRIVATE KEY-----' line is missing");
        new SigningKeys($truncated, $keys->publicKeyAsPem());
    }

    public function testIndentedPemWithCarriageReturnsLoads(): void
    {
        $keys = SigningKeys::generate();
        $indented = \implode("\r", \array_map(static fn (string $line): string => "  $line  ", \explode("\n", $keys->privateKeyAsPem())));

        self::assertSame($keys->publicKeyAsPem(), (new SigningKeys($indented, $keys->publicKeyAsPem()))->publicKeyAsPem());
    }

    private function expectValidationError(string $messageStart): void
    {
        $this->expectException(SigningKeyValidationError::class);
        $this->expectExceptionMessageMatches('/^' . \preg_quote($messageStart, '/') . '/');
    }
}
