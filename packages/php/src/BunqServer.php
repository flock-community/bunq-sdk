<?php

declare(strict_types=1);

namespace Bunq\Sdk;

/**
 * A bunq API server: its base URL and the pinned key of its TLS certificate.
 */
final readonly class BunqServer
{
    public function __construct(
        public string $baseUrl,
        public string $pinnedKey,
    ) {
    }

    /** The production server. */
    public static function public(): self
    {
        return new self('https://api.bunq.com/v1/', 'sha256/nI/T/sDfioCBHB5mVppDPyLi2HXYanwk2arpZuHLOu0=');
    }

    /** The sandbox server, for testing and development. */
    public static function sandbox(): self
    {
        return new self('https://public-api.sandbox.bunq.com/v1/', 'sha256/++MBgDH5WGvL9Bcn5Be30cRcL0f5O+NyoXuWtQdX1aI=');
    }
}
