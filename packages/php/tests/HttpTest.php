<?php

declare(strict_types=1);

namespace Bunq\Sdk\Tests;

use Bunq\Api\Wirespec;
use Bunq\Sdk\BunqApiError;
use Bunq\Sdk\Http;
use Bunq\Sdk\Signing;
use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\TestCase;

final class HttpTest extends TestCase
{
    public function test200WithResponseAndA400WithErrorAreReturnedAsIs(): void
    {
        $ok = TestServerKey::response(200, '{"Response":[]}');
        $error = TestServerKey::response(400, '{"Error":[{"error_description":"Nope"}]}');

        self::assertSame($ok, Http::requireSigned($ok, TestServerKey::publicKey()));
        self::assertSame($error, Http::requireSigned($error, TestServerKey::publicKey()));
    }

    /** @return iterable<string, array{int, string}> */
    public static function untypedResponses(): iterable
    {
        yield 'status other than 200 and 400' => [500, '{"Error":[{"error_description":"Boom"}]}'];
        yield 'html 500' => [500, '<html>Internal error</html>'];
        yield '400 that is not json' => [400, 'Bad request'];
        yield '200 without Response' => [200, '{"Error":[]}'];
        yield '400 without Error' => [400, '{"Response":[]}'];
        yield 'non-object json on a 200' => [200, '"Response"'];
    }

    #[DataProvider('untypedResponses')]
    public function testAnythingElseThrowsWithTheStatusAndTheBody(int $status, string $body): void
    {
        try {
            Http::requireTyped(new Wirespec\RawResponse($status, [], $body));
            self::fail('Expected a BunqApiError');
        } catch (BunqApiError $error) {
            self::assertSame($status, $error->status);
            self::assertSame($body, $error->body);
        }
    }

    public function testMessageTruncatesTheBodyButTheBodyFieldKeepsItWhole(): void
    {
        $body = \str_repeat('x', 2000);
        $error = new BunqApiError(502, $body);

        self::assertSame('Received 502: ' . \str_repeat('x', 500), $error->getMessage());
        self::assertSame($body, $error->body);
    }

    /** @return iterable<string, array{?string, string}> */
    public static function badSignatures(): iterable
    {
        yield 'missing' => [null, '{"Response":[]}'];
        yield 'over another body' => [TestServerKey::sign('{"Response":[{}]}'), '{"Response":[]}'];
        yield 'not base64' => ['%%%', '{"Response":[]}'];
        yield 'invalid on a 400' => [\base64_encode('nope'), '{"Error":[]}'];
    }

    #[DataProvider('badSignatures')]
    public function testResponseWithoutAValidSignatureThrows(?string $signature, string $body): void
    {
        $this->expectExceptionMessage('Invalid bunq server signature');
        Http::requireSigned(TestServerKey::response(\str_contains($body, 'Error') ? 400 : 200, $body, $signature), TestServerKey::publicKey());
    }

    public function testSignatureIsCheckedOverTheRawBodyBytes(): void
    {
        $body = "{\"Response\":[{\"name\":\"caf\u{e9}\"}]}";

        self::assertTrue(Signing::verifyResponse(TestServerKey::publicKey(), $body, TestServerKey::sign($body)));
        self::assertFalse(Signing::verifyResponse(TestServerKey::publicKey(), \json_encode(\json_decode($body)), TestServerKey::sign($body)));
    }

    public function testSignedRequestCanBeVerifiedWithThePublicKey(): void
    {
        $config = TestServerKey::config();
        $signature = Signing::signData($config, '{"secret":"s"}');

        self::assertSame(1, \openssl_verify('{"secret":"s"}', \base64_decode($signature), $config->signingKeys->publicKey(), \OPENSSL_ALGO_SHA256));
    }
}
