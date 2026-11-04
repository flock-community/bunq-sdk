<?php

declare(strict_types=1);

namespace Bunq\Sdk;

/**
 * bunq (or a proxy in front of it) answered with something other than a 200 with a `Response` or a 400 with an `Error`.
 * `headers` are the response headers with lower-case names (for example `x-bunq-client-response-id`, which bunq
 * support asks for); they are left out of the message, which ends up in logs.
 */
final class BunqApiError extends \RuntimeException
{
    /**
     * @param array<string, list<string>> $headers
     */
    public function __construct(
        public readonly int $status,
        public readonly string $body,
        public readonly array $headers = [],
    ) {
        parent::__construct(\sprintf('Received %d: %s', $status, \mb_strcut($body, 0, 500)));
    }
}
