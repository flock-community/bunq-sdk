<?php

declare(strict_types=1);

namespace Bunq\Sdk;

/**
 * Everything needed to talk to bunq: the server, the API key, the signing keys and the optional request headers.
 * `var_dump` and `print_r` show the API key and the signing keys masked; the object still holds them.
 */
final readonly class Config
{
    /**
     * @throws InvalidConfigError when the service name or the API key is blank
     */
    public function __construct(
        public BunqServer $bunqServer,
        public string $serviceName,
        #[\SensitiveParameter] public string $apiKey,
        public SigningKeys $signingKeys,
        public ?string $userAgent = null,
        public ?string $cacheControl = null,
        public ?string $language = null,
        public ?string $region = null,
        public ?string $clientRequestId = null,
        public ?string $geolocation = null,
    ) {
        if (\trim($serviceName) === '') {
            throw new InvalidConfigError('Service name cannot be blank');
        }
        if (\trim($apiKey) === '') {
            throw new InvalidConfigError('API key cannot be blank');
        }
    }

    /**
     * A config with the signing keys read from PEM strings: a PKCS#8 private key and its X.509 public key.
     */
    public static function create(
        BunqServer $bunqServer,
        string $serviceName,
        #[\SensitiveParameter] string $apiKey,
        #[\SensitiveParameter] string $privateKeyPem,
        string $publicKeyPem,
        ?string $userAgent = null,
        ?string $cacheControl = null,
        ?string $language = null,
        ?string $region = null,
        ?string $clientRequestId = null,
        ?string $geolocation = null,
    ): self {
        return new self(
            $bunqServer,
            $serviceName,
            $apiKey,
            new SigningKeys($privateKeyPem, $publicKeyPem),
            $userAgent,
            $cacheControl,
            $language,
            $region,
            $clientRequestId,
            $geolocation,
        );
    }

    /** @return array<string, mixed> */
    public function __debugInfo(): array
    {
        return ['apiKey' => '***', 'signingKeys' => '***'] + \get_object_vars($this);
    }
}
