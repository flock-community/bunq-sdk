<?php

declare(strict_types=1);

namespace Bunq\Sdk;

/**
 * The RSA key pair that signs requests to bunq. The PEM strings and the parsed keys always belong together.
 */
final class SigningKeys
{
    private const PRIVATE_KEY = 'Private key';
    private const PUBLIC_KEY = 'Public key';
    private const BOTH = 'Private and public key';
    private const PUBLIC_FROM_PRIVATE_FIX = 'openssl rsa -in private_key_pkcs8.pem -pubout -out public_key.pem';

    private readonly \OpenSSLAsymmetricKey $privateKey;
    private readonly \OpenSSLAsymmetricKey $publicKey;

    /**
     * Loads and checks a PKCS#8 private key (`-----BEGIN PRIVATE KEY-----`) and its X.509 public key (`-----BEGIN PUBLIC KEY-----`).
     *
     * @throws SigningKeyValidationError when a key cannot be read, is not RSA, or the keys do not form a pair
     */
    public function __construct(
        #[\SensitiveParameter] private readonly string $privateKeyPem,
        private readonly string $publicKeyPem,
    ) {
        $this->privateKey = self::loadPrivateKey($privateKeyPem);
        $this->publicKey = self::loadPublicKey($publicKeyPem);
        self::checkPair($this->privateKey, $this->publicKey);
    }

    /** A new 2048-bit key pair. */
    public static function generate(): self
    {
        $key = \openssl_pkey_new(['private_key_bits' => 2048, 'private_key_type' => \OPENSSL_KEYTYPE_RSA])
            ?: throw new \RuntimeException('Cannot generate an RSA key: ' . \openssl_error_string());
        \openssl_pkey_export($key, $privateKeyPem);
        return new self($privateKeyPem, \openssl_pkey_get_details($key)['key']);
    }

    /**
     * Reads the key pair from the two files, or generates one and writes it there when the files do not exist yet.
     */
    public static function fromFiles(string $privateKeyFile, string $publicKeyFile): self
    {
        if (\is_file($privateKeyFile) && \is_file($publicKeyFile)) {
            return new self((string) \file_get_contents($privateKeyFile), (string) \file_get_contents($publicKeyFile));
        }
        $keys = self::generate();
        \file_put_contents($privateKeyFile, $keys->privateKeyPem);
        \chmod($privateKeyFile, 0600);
        \file_put_contents($publicKeyFile, $keys->publicKeyPem);
        return $keys;
    }

    public function privateKeyAsPem(): string
    {
        return $this->privateKeyPem;
    }

    public function publicKeyAsPem(): string
    {
        return $this->publicKeyPem;
    }

    public function privateKey(): \OpenSSLAsymmetricKey
    {
        return $this->privateKey;
    }

    public function publicKey(): \OpenSSLAsymmetricKey
    {
        return $this->publicKey;
    }

    /** @return array<string, string> */
    public function __debugInfo(): array
    {
        return ['privateKeyPem' => '***', 'publicKeyPem' => $this->publicKeyPem];
    }

    /** Loads an X.509 RSA public key, such as the server public key bunq returns. */
    public static function loadPublicKey(string $pem): \OpenSSLAsymmetricKey
    {
        $der = self::readPemBody($pem, 'PUBLIC KEY', self::PUBLIC_KEY);
        $key = \openssl_pkey_get_public(self::toPem($der, 'PUBLIC KEY'));
        return self::requireRsa($key, self::PUBLIC_KEY, 'Derive it with: ' . self::PUBLIC_FROM_PRIVATE_FIX);
    }

    private static function loadPrivateKey(string $pem): \OpenSSLAsymmetricKey
    {
        $der = self::readPemBody($pem, 'PRIVATE KEY', self::PRIVATE_KEY);
        $key = \openssl_pkey_get_private(self::toPem($der, 'PRIVATE KEY'));
        return self::requireRsa($key, self::PRIVATE_KEY, 'Generate one with: openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048');
    }

    private static function requireRsa(\OpenSSLAsymmetricKey|false $key, string $keyType, string $hint): \OpenSSLAsymmetricKey
    {
        $type = $key === false ? null : (\openssl_pkey_get_details($key)['type'] ?? null);
        if ($key === false || $type !== \OPENSSL_KEYTYPE_RSA) {
            $reason = $key === false ? (\openssl_error_string() ?: 'unreadable key') : 'not an RSA key';
            throw new SigningKeyValidationError(
                "not a valid RSA key ($reason). The key may be truncated or corrupted, or not an RSA key (only RSA keys are supported). $hint",
                $keyType,
                'RSA validation',
            );
        }
        return $key;
    }

    private static function toPem(string $der, string $label): string
    {
        return "-----BEGIN $label-----\n" . \chunk_split(\base64_encode($der), 64, "\n") . "-----END $label-----\n";
    }

    /** The DER bytes of the first PEM block, which must have the expected label. */
    private static function readPemBody(string $pem, string $label, string $keyType): string
    {
        $invalid = static fn (string $detail): SigningKeyValidationError => new SigningKeyValidationError($detail, $keyType, 'PEM parsing');
        if (\str_contains($pem, '\n')) {
            throw $invalid('the PEM contains literal \n sequences; replace them with real newlines');
        }
        $lines = \array_values(\array_filter(\array_map('trim', \preg_split('/\r\n|\r|\n/', $pem) ?: []), static fn (string $line): bool => $line !== ''));
        if (\count($lines) < 2) {
            throw $invalid('the PEM has no line breaks; put the BEGIN line, the base64 body and the END line on separate lines');
        }
        $begin = null;
        foreach ($lines as $index => $line) {
            if (\preg_match('/^-----BEGIN (.+)-----$/', $line, $match) === 1) {
                $begin = [$index, $match[1]];
                break;
            }
        }
        if ($begin === null) {
            throw $invalid('no PEM block could be read; check that the BEGIN line is present and the line breaks are real newlines');
        }
        [$beginIndex, $blockType] = $begin;
        $end = \array_search("-----END $blockType-----", \array_slice($lines, $beginIndex + 1), true);
        if ($end === false) {
            throw $invalid("the '-----END $label-----' line is missing, the PEM looks truncated");
        }
        $body = \array_slice($lines, $beginIndex + 1, (int) $end);
        $headers = \array_filter($body, static fn (string $line): bool => \str_contains($line, ':'));
        $content = \base64_decode(\implode('', \array_filter($body, static fn (string $line): bool => !\str_contains($line, ':'))), true);
        if ($content === false) {
            throw $invalid('the body is not valid base64 or is malformed. Re-export the key without modifying it.');
        }

        $encrypted = $blockType === 'ENCRYPTED PRIVATE KEY' || \array_filter($headers, static fn (string $h): bool => \str_starts_with($h, 'Proc-Type:') && \str_contains($h, 'ENCRYPTED')) !== [];
        $expectsPrivate = $keyType === self::PRIVATE_KEY;
        return match (true) {
            $blockType === $label && !$encrypted => $content,
            $encrypted && $expectsPrivate => throw $invalid('the key is encrypted, which is not supported. Decrypt it first (the command asks for the passphrase): openssl pkcs8 -topk8 -nocrypt -in encrypted_key.pem -out private_key_pkcs8.pem'),
            $blockType === 'RSA PRIVATE KEY' && $expectsPrivate => throw $invalid("the key is in PKCS#1 format but PKCS#8 ('-----BEGIN PRIVATE KEY-----') is required. Convert it with: openssl pkcs8 -topk8 -inform PEM -outform PEM -nocrypt -in private_key.pem -out private_key_pkcs8.pem"),
            $blockType === 'RSA PUBLIC KEY' && !$expectsPrivate => throw $invalid("the key is in PKCS#1 format but X.509 ('-----BEGIN PUBLIC KEY-----') is required. Convert it with: openssl rsa -RSAPublicKey_in -in public_key.pem -pubout -out public_key_spki.pem"),
            $expectsPrivate && \str_ends_with($blockType, 'PUBLIC KEY') => throw $invalid('this is a public key, a private key is expected. The keys may be swapped.'),
            !$expectsPrivate && \str_ends_with($blockType, 'PRIVATE KEY') => throw $invalid('this is a private key, a public key is expected. The keys may be swapped. Derive the public key with: ' . self::PUBLIC_FROM_PRIVATE_FIX),
            default => throw $invalid("the first PEM block is '$blockType' but '$label' is expected"),
        };
    }

    private static function checkPair(\OpenSSLAsymmetricKey $privateKey, \OpenSSLAsymmetricKey $publicKey): void
    {
        $public = \openssl_pkey_get_details($publicKey)['rsa'];
        if (\bin2hex($public['e']) !== '010001') {
            throw new SigningKeyValidationError('unexpected public exponent. Expected 65537, got 0x' . \bin2hex($public['e']), self::PUBLIC_KEY, 'RSA validation');
        }
        if (\openssl_pkey_get_details($privateKey)['rsa']['n'] !== $public['n']) {
            throw new SigningKeyValidationError('the keys do not form a pair (the moduli differ). Derive the public key with: ' . self::PUBLIC_FROM_PRIVATE_FIX, self::BOTH, 'compatibility check');
        }
    }
}
