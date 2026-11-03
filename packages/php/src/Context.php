<?php

declare(strict_types=1);

namespace Bunq\Sdk;

/**
 * A bunq session with the installation and device it belongs to. `var_dump` and `print_r` show the session token,
 * the installation token and the config secrets masked; the object still holds them, so store it as a secret.
 */
final readonly class Context
{
    public function __construct(
        public string $serverPublicKey,
        public int $deviceId,
        public int $sessionId,
        #[\SensitiveParameter] public string $sessionToken,
        public int $userId,
        public \DateTimeImmutable $sessionExpiryTime,
        #[\SensitiveParameter] public string $installationToken,
        public Config $config,
    ) {
    }

    /** @return array<string, mixed> */
    public function __debugInfo(): array
    {
        return ['sessionToken' => '***', 'installationToken' => '***'] + \get_object_vars($this);
    }
}
