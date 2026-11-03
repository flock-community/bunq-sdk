<?php

declare(strict_types=1);

namespace Bunq\Sdk;

/**
 * bunq (or a proxy in front of it) answered with something other than a 200 with a `Response` or a 400 with an `Error`.
 */
final class BunqApiError extends \RuntimeException
{
    public function __construct(
        public readonly int $status,
        public readonly string $body,
    ) {
        parent::__construct(\sprintf('Received %d: %s', $status, \mb_strcut($body, 0, 500)));
    }
}
