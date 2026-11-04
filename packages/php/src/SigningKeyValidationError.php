<?php

declare(strict_types=1);

namespace Bunq\Sdk;

/**
 * A signing key is rejected: "<key> validation failed during <stage>: <detail>".
 */
final class SigningKeyValidationError extends InvalidConfigError
{
    public function __construct(
        string $detail,
        public readonly string $keyType,
        public readonly string $stage,
    ) {
        parent::__construct("$keyType validation failed during $stage: $detail");
    }
}
