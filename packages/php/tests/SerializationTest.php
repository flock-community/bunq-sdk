<?php

declare(strict_types=1);

namespace Bunq\Sdk\Tests;

use Bunq\Api\Endpoint\ListAllPaymentForUserMonetaryAccount;
use Bunq\Api\Endpoint\ReadUser;
use Bunq\Api\Model\Amount;
use Bunq\Api\Model\CreateInstallation400ResponseBody;
use Bunq\Api\Model\DeviceServer;
use Bunq\Api\Model\InstallationCreate;
use Bunq\Api\Model\PaymentListing;
use Bunq\Api\Model\PaymentPage;
use Bunq\Api\Wirespec;
use Bunq\Sdk\Serialization;
use PHPUnit\Framework\TestCase;

final class SerializationTest extends TestCase
{
    private Serialization $serialization;

    protected function setUp(): void
    {
        $this->serialization = new Serialization();
    }

    public function testSingleResultMergesTheObjectsOfTheResponse(): void
    {
        $body = '{"Response":[{"Id":{"id":7}},{"Token":{"id":8,"token":"abc"}},{"ServerPublicKey":{"server_public_key":"pem"}}]}';

        $installation = $this->serialization->deserializeBody($body, InstallationCreate::class);

        self::assertInstanceOf(InstallationCreate::class, $installation);
        self::assertSame(7, $installation->Id?->id);
        self::assertSame('abc', $installation->Token?->token);
        self::assertSame('pem', $installation->ServerPublicKey?->server_public_key);
    }

    public function testListResponseKeepsTheItemsAndThePaginationBlock(): void
    {
        $body = '{"Response":[{"Payment":{"id":2,"amount":{"value":"-1.50","currency":"EUR"}}},{"Payment":{"id":1,"description":"first"}}],'
            . '"Pagination":{"future_url":null,"newer_url":"/v1/user/1/monetary-account/2/payment?newer_id=2","older_url":null}}';

        $page = $this->serialization->deserializeBody($body, PaymentPage::class);

        self::assertInstanceOf(PaymentPage::class, $page);
        self::assertContainsOnlyInstancesOf(PaymentListing::class, $page->Response);
        self::assertSame([2, 1], \array_map(static fn (PaymentListing $payment): ?int => $payment->id, $page->Response));
        self::assertEquals(new Amount(value: '-1.50', currency: 'EUR'), $page->Response[0]->amount);
        self::assertNull($page->Response[1]->amount);
        self::assertSame('first', $page->Response[1]->description);
        self::assertSame('/v1/user/1/monetary-account/2/payment?newer_id=2', $page->Pagination->newer_url);
        self::assertNull($page->Pagination->older_url);
    }

    public function testEmptyPageHasAnEmptyListAndItsPagination(): void
    {
        $page = $this->serialization->deserializeBody('{"Response":[],"Pagination":{"future_url":null,"newer_url":null,"older_url":null}}', PaymentPage::class);

        self::assertSame([], $page->Response);
        self::assertNull($page->Pagination->newer_url);
    }

    public function testListTypeTakesTheValueOfEachItem(): void
    {
        $amounts = $this->serialization->deserializeBody('{"Response":[{"Amount":{"value":"1"}},{"Amount":{"value":"2"}}]}', 'list<' . Amount::class . '>');

        self::assertEquals([new Amount(value: '1', currency: null), new Amount(value: '2', currency: null)], $amounts);
    }

    public function testErrorBodyWithoutResponseEnvelopeIsTheDocumentItself(): void
    {
        $error = $this->serialization->deserializeBody('{"Error":[{"error_description":"Nope","error_description_translated":"Nee"}]}', CreateInstallation400ResponseBody::class);

        self::assertSame('Nope', $error->Error[0]->error_description);
    }

    public function testBodyWithoutResponseOrErrorIsRejected(): void
    {
        $this->expectExceptionMessage('neither Response nor Error');
        $this->serialization->deserializeBody('{"Something":1}', InstallationCreate::class);
    }

    public function testBodyThatIsNotAnObjectIsRejected(): void
    {
        $this->expectExceptionMessage('neither Response nor Error');
        $this->serialization->deserializeBody('[1,2]', InstallationCreate::class);
    }

    public function testSerializedBodyLeavesOutNullFields(): void
    {
        $json = $this->serialization->serializeBody(new DeviceServer(description: 'PhpTest', secret: 's3cret', permitted_ips: null), DeviceServer::class);

        self::assertSame('{"description":"PhpTest","secret":"s3cret"}', $json);
    }

    public function testParamsAndPathsUseTheTypeString(): void
    {
        self::assertSame(['42'], $this->serialization->serializeParam(42, 'int'));
        self::assertSame(['true'], $this->serialization->serializeParam(true, 'bool'));
        self::assertSame(['a', 'b'], $this->serialization->serializeParam(['a', 'b'], 'list<string>'));
        self::assertSame(['PUT'], $this->serialization->serializeParam(Wirespec\Method::PUT, Wirespec\Method::class));
        self::assertSame(42, $this->serialization->deserializeParam(['42'], 'int'));
        self::assertSame([1, 2], $this->serialization->deserializeParam(['1', '2'], 'list<int>'));
        self::assertSame(Wirespec\Method::PATCH, $this->serialization->deserializeParam(['PATCH'], Wirespec\Method::class));
        self::assertSame('7', $this->serialization->serializePath(7, 'int'));
        self::assertSame(7, $this->serialization->deserializePath('7', 'int'));
        self::assertNull($this->serialization->deserializeParam([], 'int'));
    }

    public function testGeneratedEndpointRoundTripsThroughRawRequestAndResponse(): void
    {
        $raw = ListAllPaymentForUserMonetaryAccount::toRawRequest($this->serialization, new ListAllPaymentForUserMonetaryAccount\Request(1, 2, 10, null, 5));

        self::assertSame('GET', $raw->method);
        self::assertSame(['user', '1', 'monetary-account', '2', 'payment'], $raw->path);
        self::assertSame(['count' => ['10'], 'newer_id' => [], 'older_id' => ['5']], $raw->queries);
        self::assertNull($raw->body);

        $request = ListAllPaymentForUserMonetaryAccount::fromRawRequest($this->serialization, $raw);
        self::assertSame([1, 2, 10, null, 5], [$request->path->userID, $request->path->monetaryAccountID, $request->queries->count, $request->queries->newer_id, $request->queries->older_id]);

        $response = ReadUser::fromRawResponse($this->serialization, new Wirespec\RawResponse(200, [], '{"Response":[{"UserPerson":{"id":3,"display_name":"Peter"}}]}'));
        self::assertInstanceOf(ReadUser\Response200::class, $response);
        self::assertSame('Peter', $response->body->UserPerson?->display_name);
    }
}
