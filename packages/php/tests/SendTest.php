<?php

declare(strict_types=1);

namespace Bunq\Sdk\Tests;

use Bunq\Api\Wirespec;
use Bunq\Sdk\Config;
use Bunq\Sdk\Http;
use PHPUnit\Framework\TestCase;

/**
 * Sends real HTTP requests to PHP's built-in server, which answers with what it received.
 */
final class SendTest extends TestCase
{
    /** @var resource|null */
    private static $server = null;
    private static string $baseUrl = '';

    public static function setUpBeforeClass(): void
    {
        $port = self::freePort();
        self::$server = \proc_open([\PHP_BINARY, '-S', "127.0.0.1:$port", __DIR__ . '/fixtures/echo-server.php'], [1 => ['file', '/dev/null', 'w'], 2 => ['file', '/dev/null', 'w']], $pipes);
        self::$baseUrl = "http://127.0.0.1:$port/v1/";
        for ($attempt = 0; $attempt < 50 && @\fsockopen('127.0.0.1', $port) === false; $attempt++) {
            \usleep(100_000);
        }
    }

    public static function tearDownAfterClass(): void
    {
        if (self::$server !== null) {
            \proc_terminate(self::$server);
        }
    }

    public function testSendsQueryHeadersAndSignsARequestWithABody(): void
    {
        $config = TestServerKey::config(self::$baseUrl);
        $response = Http::send($config, new Wirespec\RawRequest('POST', ['user', '1', 'payment'], ['count' => ['10'], 'ids' => ['1', '2']], ['X-Custom' => ['yes'], 'X-Blank' => [' ']], '{"amount":1}'));
        $received = \json_decode((string) $response->body, true);

        self::assertSame(200, $response->statusCode);
        self::assertSame('POST', $received['method']);
        self::assertSame('/v1/user/1/payment?count=10&ids=1&ids=2', $received['uri']);
        self::assertSame('{"amount":1}', $received['body']);
        self::assertSame('yes', $received['headers']['x-custom']);
        self::assertArrayNotHasKey('x-blank', $received['headers']);
        self::assertSame(1, \openssl_verify('{"amount":1}', \base64_decode($received['headers']['x-bunq-client-signature']), $config->signingKeys->publicKey(), \OPENSSL_ALGO_SHA256));
        self::assertSame(['application/json'], $response->headers['content-type']);
    }

    public function testDoesNotSignARequestWithoutABody(): void
    {
        $received = \json_decode((string) Http::send(TestServerKey::config(self::$baseUrl), new Wirespec\RawRequest('GET', ['user'], [], [], null))->body, true);

        self::assertSame('GET', $received['method']);
        self::assertArrayNotHasKey('x-bunq-client-signature', $received['headers']);
    }

    public function testQueryWithoutValuesAddsNoQuestionMark(): void
    {
        $received = \json_decode((string) Http::send(TestServerKey::config(self::$baseUrl), new Wirespec\RawRequest('GET', ['user'], ['count' => [], 'older_id' => []], [], null))->body, true);

        self::assertSame('/v1/user', $received['uri']);
    }

    public function testRequestTimeoutStopsASlowResponse(): void
    {
        $config = TestServerKey::config(self::$baseUrl);
        $slow = new Config($config->bunqServer, $config->serviceName, $config->apiKey, $config->signingKeys, requestTimeout: 0.2);

        $this->expectExceptionMessageMatches('/timed out/i');
        Http::send($slow, new Wirespec\RawRequest('GET', ['user'], ['delay' => ['2000']], [], null));
    }

    public function testUserAgentDefaultsToTheServiceName(): void
    {
        self::assertSame('PhpTest', $this->userAgent(null));
        self::assertSame('PhpTest', $this->userAgent('   '));
        self::assertSame('MyApp/1.0', $this->userAgent('MyApp/1.0'));
    }

    private function userAgent(?string $configured): string
    {
        $response = Http::send(TestServerKey::config(self::$baseUrl, $configured), new Wirespec\RawRequest('GET', ['user'], [], [], null));
        return \json_decode((string) $response->body, true)['headers']['user-agent'];
    }

    private static function freePort(): int
    {
        $socket = \stream_socket_server('tcp://127.0.0.1:0');
        $port = (int) \substr((string) \stream_socket_get_name($socket, false), \strrpos((string) \stream_socket_get_name($socket, false), ':') + 1);
        \fclose($socket);
        return $port;
    }
}
