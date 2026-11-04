<?php

declare(strict_types=1);

namespace Bunq\Sdk;

use Bunq\Api\Wirespec;

/**
 * Sends requests with the context's authentication headers.
 *
 * A session that has expired (or expires within 30 seconds) is refreshed before the request is sent. A 403
 * "Insufficient authentication." refreshes the session once and retries the request with the new token. Statuses
 * other than 200 and 400, including the original 403 when the refresh fails (a failed refresh before sending is not
 * repeated after a 403 in the same request), are thrown as {@see BunqApiError}. Every 200/400 response must carry a
 * valid `X-Bunq-Server-Signature`. The refreshed context is kept inside this transportation, so later requests use
 * the new token, and $onContextChange is called once with every new context so the caller can store it.
 */
final class BunqTransportation implements Wirespec\Transportation
{
    private const SESSION_REJECTION = 'Insufficient authentication.';
    private const EXPIRY_MARGIN = 'PT30S';

    private Context $current;

    /**
     * @param \Closure(Context): Context $refresh
     * @param (\Closure(Context): void)|null $onContextChange
     * @param (\Closure(Config, Wirespec\RawRequest): Wirespec\RawResponse)|null $send
     */
    public function __construct(
        Context $context,
        private readonly \Closure $refresh,
        private readonly ?\Closure $onContextChange = null,
        private readonly ?\Closure $send = null,
    ) {
        $this->current = $context;
    }

    public function context(): Context
    {
        return $this->current;
    }

    public function transport(Wirespec\RawRequest $request): Wirespec\RawResponse
    {
        $snapshot = $this->current;
        // null when the refresh before sending failed: a 403 then does not trigger a second refresh in the same request
        $preRefreshed = $snapshot->sessionExpiryTime <= (new \DateTimeImmutable())->add(new \DateInterval(self::EXPIRY_MARGIN))
            ? $this->refreshed($snapshot)
            : $snapshot;
        $used = $preRefreshed ?? $snapshot;
        $response = $this->sendWith($used, $request);
        if ($preRefreshed === null || !self::isSessionRejected($response)) {
            return Http::requireSigned($response, $used->serverPublicKey);
        }
        $fresh = $this->refreshed($used);
        return $fresh === null
            ? Http::requireSigned($response, $used->serverPublicKey)
            : Http::requireSigned($this->sendWith($fresh, $request), $fresh->serverPublicKey);
    }

    /** The refreshed context, or null when the refresh failed. */
    private function refreshed(Context $used): ?Context
    {
        // another request may have refreshed already; compared by identity because bunq returns the same session token on a re-created session
        if ($this->current !== $used) {
            return $this->current;
        }
        try {
            $fresh = ($this->refresh)($used);
        } catch (\Throwable $e) {
            \error_log("bunq session refresh failed: {$e->getMessage()}");
            return null;
        }
        $this->current = $fresh;
        if ($this->onContextChange !== null) {
            ($this->onContextChange)($fresh);
        }
        return $fresh;
    }

    private function sendWith(Context $used, Wirespec\RawRequest $request): Wirespec\RawResponse
    {
        $authenticated = new Wirespec\RawRequest(
            method: $request->method,
            path: $request->path,
            queries: $request->queries,
            headers: [...$request->headers, ...self::authenticationHeaders($used)],
            body: $request->body,
        );
        return $this->send === null ? Http::send($used->config, $authenticated) : ($this->send)($used->config, $authenticated);
    }

    /** @return array<string, list<string>> */
    private static function authenticationHeaders(Context $context): array
    {
        $config = $context->config;
        return \array_map(static fn (string $value): array => [$value], \array_filter([
            'X-Bunq-Client-Authentication' => $context->sessionToken,
            'Cache-Control' => $config->cacheControl,
            'X-Bunq-Language' => $config->language,
            'X-Bunq-Region' => $config->region,
            'X-Bunq-Client-Request-Id' => $config->clientRequestId,
            'X-Bunq-Geolocation' => $config->geolocation,
        ], static fn (?string $value): bool => $value !== null && $value !== ''));
    }

    // bunq answers a dead session with 403 and this error description; other 403s are real permission errors
    private static function isSessionRejected(Wirespec\RawResponse $response): bool
    {
        if ($response->statusCode !== 403 || $response->body === null) {
            return false;
        }
        $errors = \json_decode($response->body, true)['Error'] ?? null;
        return \is_array($errors) && \in_array(self::SESSION_REJECTION, \array_column($errors, 'error_description'), true);
    }
}
