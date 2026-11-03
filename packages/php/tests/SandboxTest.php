<?php

declare(strict_types=1);

namespace Bunq\Sdk\Tests;

use Bunq\Api\Client;
use Bunq\Api\Endpoint\CreateSandboxUserPerson;
use Bunq\Api\Endpoint\ListAllMonetaryAccountBankForUser;
use Bunq\Api\Endpoint\ReadUser;
use Bunq\Api\Model\SandboxUserPerson;
use Bunq\Api\Wirespec;
use Bunq\Sdk\Bunq;
use Bunq\Sdk\BunqServer;
use Bunq\Sdk\Config;
use Bunq\Sdk\Context;
use Bunq\Sdk\Http;
use Bunq\Sdk\Serialization;
use Bunq\Sdk\SigningKeys;
use PHPUnit\Framework\Attributes\Group;
use PHPUnit\Framework\TestCase;

/**
 * Calls the bunq sandbox with a fresh sandbox user.
 */
#[Group('sandbox')]
final class SandboxTest extends TestCase
{
    private static Context $context;

    public static function setUpBeforeClass(): void
    {
        $keys = SigningKeys::generate();
        self::$context = Bunq::initContext(new Config(BunqServer::sandbox(), 'PhpSdkTest', self::newSandboxApiKey($keys), $keys));
    }

    public function testReadUser(): void
    {
        $response = Bunq::client(self::$context)->readUser(self::$context->userId);

        self::assertInstanceOf(ReadUser\Response200::class, $response);
        self::assertNotEmpty($response->body->UserPerson?->display_name);
        self::assertSame([], $response->body->validate());
    }

    public function testListAllMonetaryAccountBankForUser(): void
    {
        $response = Bunq::client(self::$context)->listAllMonetaryAccountBankForUser(self::$context->userId, null, null, null);

        self::assertInstanceOf(ListAllMonetaryAccountBankForUser\Response200::class, $response);
        self::assertNotEmpty($response->body->Response[0]->display_name);
        self::assertSame('EUR', $response->body->Response[0]->currency);
    }

    public function testRefreshedSessionKeepsTheDeviceAndInstallation(): void
    {
        $refreshed = Bunq::refreshSession(self::$context);

        self::assertNotSame(self::$context->sessionId, $refreshed->sessionId);
        self::assertSame(self::$context->deviceId, $refreshed->deviceId);
        self::assertSame(self::$context->installationToken, $refreshed->installationToken);
        self::assertInstanceOf(ReadUser\Response200::class, Bunq::client($refreshed)->readUser($refreshed->userId));
    }

    /** One fresh sandbox user per test class: bunq answers 429 when several clients set up sessions with one API key at the same time. */
    private static function newSandboxApiKey(SigningKeys $keys): string
    {
        $config = new Config(BunqServer::sandbox(), 'PhpSdkTest', 'unused', $keys);
        $response = (new Client(new Serialization(), new class ($config) implements Wirespec\Transportation {
            public function __construct(private readonly Config $config)
            {
            }

            public function transport(Wirespec\RawRequest $request): Wirespec\RawResponse
            {
                // no session and no server public key exist yet, so this one call is not signature-verified
                return Http::requireTyped(Http::send($this->config, $request));
            }
        }))->createSandboxUserPerson(new SandboxUserPerson());

        return $response instanceof CreateSandboxUserPerson\Response200 && $response->body->ApiKey?->api_key !== null
            ? $response->body->ApiKey->api_key
            : throw new \RuntimeException('Cannot create a sandbox user');
    }
}
