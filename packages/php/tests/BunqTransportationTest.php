<?php

declare(strict_types=1);

namespace Bunq\Sdk\Tests;

use Bunq\Api\Wirespec;
use Bunq\Sdk\BunqApiError;
use Bunq\Sdk\BunqTransportation;
use Bunq\Sdk\Config;
use Bunq\Sdk\Context;
use PHPUnit\Framework\TestCase;

final class BunqTransportationTest extends TestCase
{
    private const REJECTED = '{"Error":[{"error_description":"Insufficient authentication.","error_description_translated":"Insufficient authentication."}]}';
    private const OK = '{"Response":[{"Id":{"id":1}}]}';

    /** @var list<string> the session token of every request sent */
    private array $sentTokens = [];
    private int $refreshes = 0;
    /** @var list<Context> */
    private array $changes = [];

    public function testSessionRejectedRefreshesOnceAndRetriesWithTheNewToken(): void
    {
        $transportation = $this->transportation(TestServerKey::context(), [403 => self::REJECTED], fn (Context $c): Context => $this->refreshTo($c, 'session-2'));

        $response = $transportation->transport($this->request());

        self::assertSame(200, $response->statusCode);
        self::assertSame(['session-1', 'session-2'], $this->sentTokens);
        self::assertSame(1, $this->refreshes);
        self::assertSame(['session-2'], \array_map(static fn (Context $c): string => $c->sessionToken, $this->changes));
    }

    public function testLaterRequestsUseTheRefreshedToken(): void
    {
        $transportation = $this->transportation(TestServerKey::context(), [403 => self::REJECTED], fn (Context $c): Context => $this->refreshTo($c, 'session-2'));

        $transportation->transport($this->request());
        $transportation->transport($this->request());

        self::assertSame(['session-1', 'session-2', 'session-2'], $this->sentTokens);
        self::assertSame('session-2', $transportation->context()->sessionToken);
    }

    public function testFailedRefreshThrowsTheOriginal403(): void
    {
        $transportation = $this->transportation(TestServerKey::context(), [403 => self::REJECTED], static fn (Context $c): Context => throw new \RuntimeException('bunq is down'));

        try {
            $transportation->transport($this->request());
            self::fail('Expected a BunqApiError');
        } catch (BunqApiError $error) {
            self::assertSame(403, $error->status);
            self::assertSame(self::REJECTED, $error->body);
        }
        self::assertSame([], $this->changes);
    }

    public function testOtherForbiddenResponsesDoNotRefresh(): void
    {
        foreach (['{"Error":[{"error_description":"Not allowed."}]}', '', '<html>Forbidden</html>'] as $body) {
            $transportation = $this->transportation(TestServerKey::context(), [403 => $body], fn (Context $c): Context => $this->refreshTo($c, 'session-2'));
            try {
                $transportation->transport($this->request());
                self::fail('Expected a BunqApiError');
            } catch (BunqApiError $error) {
                self::assertSame(403, $error->status);
            }
        }
        self::assertSame(0, $this->refreshes);
    }

    public function testUnsignedResponseAfterTheRefreshThrows(): void
    {
        $transportation = $this->transportation(TestServerKey::context(), [403 => self::REJECTED], fn (Context $c): Context => $this->refreshTo($c, 'session-2'), signed: false);

        $this->expectExceptionMessage('Invalid bunq server signature');
        $transportation->transport($this->request());
    }

    public function testExpiredContextIsRefreshedBeforeTheFirstRequestAndTheCallbackFiresOnce(): void
    {
        $transportation = $this->transportation(TestServerKey::context(expiresIn: '-1 minute'), [], fn (Context $c): Context => $this->refreshTo($c, 'session-2'));

        $transportation->transport($this->request());
        $transportation->transport($this->request());

        self::assertSame(['session-2', 'session-2'], $this->sentTokens);
        self::assertSame(1, $this->refreshes);
        self::assertCount(1, $this->changes);
    }

    public function testContextExpiringWithinTheMarginIsRefreshed(): void
    {
        $this->transportation(TestServerKey::context(expiresIn: '+10 seconds'), [], fn (Context $c): Context => $this->refreshTo($c, 'session-2'))->transport($this->request());

        self::assertSame(['session-2'], $this->sentTokens);
    }

    public function testContextThatIsNotExpiredIsNotRefreshed(): void
    {
        $this->transportation(TestServerKey::context(expiresIn: '+10 minutes'), [], fn (Context $c): Context => $this->refreshTo($c, 'session-2'))->transport($this->request());

        self::assertSame(['session-1'], $this->sentTokens);
        self::assertSame(0, $this->refreshes);
    }

    public function testFailedRefreshBeforeSendingIsNotRepeatedAfterThe403(): void
    {
        $transportation = $this->transportation(TestServerKey::context(expiresIn: '-1 minute'), [403 => self::REJECTED], function (Context $c): Context {
            $this->refreshes++;
            throw new \RuntimeException('bunq is down');
        });

        try {
            $transportation->transport($this->request());
            self::fail('Expected a BunqApiError');
        } catch (BunqApiError $error) {
            self::assertSame(403, $error->status);
        }
        self::assertSame(1, $this->refreshes);
    }

    public function testAuthenticationAndConfiguredHeadersAreSent(): void
    {
        $headers = [];
        $context = TestServerKey::context();
        $config = $context->config;
        $withLanguage = new Context($context->serverPublicKey, 1, 2, 'session-1', 3, $context->sessionExpiryTime, 'installation',
            new Config($config->bunqServer, $config->serviceName, $config->apiKey, $config->signingKeys, language: 'nl_NL'));
        (new BunqTransportation($withLanguage, static fn (Context $c): Context => $c, null, static function (Config $config, Wirespec\RawRequest $request) use (&$headers): Wirespec\RawResponse {
            $headers = $request->headers;
            return TestServerKey::response(200, self::OK);
        }))->transport($this->request());

        self::assertSame(['X-Custom' => ['yes'], 'X-Bunq-Client-Authentication' => ['session-1'], 'X-Bunq-Language' => ['nl_NL']], $headers);
    }

    /**
     * @param array<int, string> $failures the response for the first request with the original session token, by status
     * @param \Closure(Context): Context $refresh
     */
    private function transportation(Context $context, array $failures, \Closure $refresh, bool $signed = true): BunqTransportation
    {
        $send = function (Config $config, Wirespec\RawRequest $request) use ($failures, $signed): Wirespec\RawResponse {
            $token = $request->headers['X-Bunq-Client-Authentication'][0];
            $this->sentTokens[] = $token;
            foreach ($failures as $status => $body) {
                if ($token === 'session-1') {
                    return TestServerKey::response($status, $body);
                }
            }
            return TestServerKey::response(200, self::OK, $signed ? 'valid' : null);
        };
        return new BunqTransportation($context, $refresh, function (Context $context): void {
            $this->changes[] = $context;
        }, $send);
    }

    private function refreshTo(Context $context, string $token): Context
    {
        $this->refreshes++;
        return new Context($context->serverPublicKey, $context->deviceId, $context->sessionId + 1, $token, $context->userId, new \DateTimeImmutable('+1 hour'), $context->installationToken, $context->config);
    }

    private function request(): Wirespec\RawRequest
    {
        return new Wirespec\RawRequest('GET', ['user', '3'], [], ['X-Custom' => ['yes']], null);
    }
}
