<?php

declare(strict_types=1);

namespace Bunq\Sdk;

use Bunq\Api\Client;
use Bunq\Api\Endpoint\CreateDeviceServer;
use Bunq\Api\Endpoint\CreateInstallation;
use Bunq\Api\Endpoint\CreateSessionServer;
use Bunq\Api\Model\DeviceServer;
use Bunq\Api\Model\DeviceServerCreate;
use Bunq\Api\Model\Installation;
use Bunq\Api\Model\InstallationCreate;
use Bunq\Api\Model\SessionServer;
use Bunq\Api\Model\SessionServerCreate;
use Bunq\Api\Model\UserApiKeyAnchoredUser;
use Bunq\Api\Wirespec;

/**
 * Entry point of the SDK: create a context once, then call bunq through the generated client.
 *
 *     $context = Bunq::initContext($config);
 *     $user = Bunq::client($context)->readUser($context->userId);
 */
final class Bunq
{
    private const DEFAULT_SESSION_TIMEOUT_SECONDS = 30 * 60;

    /**
     * The client Wirespec generates, with one method per bunq operation. It sends the context's session token,
     * refreshes the session when it has expired or bunq rejects it, and calls $onContextChange with every new context.
     *
     * @param (\Closure(Context): void)|null $onContextChange
     */
    public static function client(Context $context, ?\Closure $onContextChange = null): Client
    {
        return new Client(new Serialization(), new BunqTransportation($context, self::refreshSession(...), $onContextChange));
    }

    /**
     * Registers an installation and a device for the config's API key and starts a session. Store the context and
     * build the client from it on the next start: the installation and the device are only needed once.
     */
    public static function initContext(Config $config): Context
    {
        $installation = self::createInstallation($config);
        $serverPublicKey = $installation->ServerPublicKey?->server_public_key ?: throw new \UnexpectedValueException('No server public key');
        $installationToken = $installation->Token?->token ?: throw new \UnexpectedValueException('Token not available');

        $device = self::createDeviceServer($config, $installationToken, $serverPublicKey);
        $deviceId = $device->Id?->id ?? throw new \UnexpectedValueException('No device id');

        return self::startSession($config, $installationToken, $serverPublicKey, $deviceId);
    }

    /**
     * A new session for the same installation and device. A client made earlier keeps its own context; make a new
     * client from the returned one.
     */
    public static function refreshSession(Context $context): Context
    {
        return self::startSession($context->config, $context->installationToken, $context->serverPublicKey, $context->deviceId);
    }

    private static function startSession(Config $config, string $installationToken, string $serverPublicKey, int $deviceId): Context
    {
        $response = self::setupClient($config, $installationToken, $serverPublicKey)->createSessionServer(new SessionServer(secret: $config->apiKey));
        $session = $response instanceof CreateSessionServer\Response200
            ? $response->body
            : throw new \RuntimeException(self::setupFailure('Session server creation failed', $response));

        return new Context(
            serverPublicKey: $serverPublicKey,
            deviceId: $deviceId,
            sessionId: $session->Id?->id ?? throw new \UnexpectedValueException('No session id'),
            sessionToken: $session->Token?->token ?? throw new \UnexpectedValueException('No session token'),
            userId: self::userId($session),
            sessionExpiryTime: new \DateTimeImmutable(\sprintf('+%d seconds', self::sessionTimeout($session))),
            installationToken: $installationToken,
            config: $config,
        );
    }

    private static function createInstallation(Config $config): InstallationCreate
    {
        $response = self::setupClient($config)->createInstallation(new Installation(client_public_key: $config->signingKeys->publicKeyAsPem()));
        return $response instanceof CreateInstallation\Response200
            ? $response->body
            : throw new \RuntimeException(self::setupFailure('Installation failed', $response));
    }

    private static function createDeviceServer(Config $config, string $installationToken, string $serverPublicKey): DeviceServerCreate
    {
        $response = self::setupClient($config, $installationToken, $serverPublicKey)
            ->createDeviceServer(new DeviceServer(description: $config->serviceName, secret: $config->apiKey, permitted_ips: ['*']));
        return $response instanceof CreateDeviceServer\Response200
            ? $response->body
            : throw new \RuntimeException(self::setupFailure('Device server creation failed', $response));
    }

    /**
     * A client for the requests that build a context: they carry the installation token, if any, instead of a session
     * token. The server public key is not known yet for the installation call, so that response is not verified.
     */
    private static function setupClient(Config $config, ?string $installationToken = null, ?string $serverPublicKey = null): Client
    {
        return new Client(new Serialization(), new class ($config, $installationToken, $serverPublicKey) implements Wirespec\Transportation {
            public function __construct(
                private readonly Config $config,
                private readonly ?string $installationToken,
                private readonly ?string $serverPublicKey,
            ) {
            }

            public function transport(Wirespec\RawRequest $request): Wirespec\RawResponse
            {
                $headers = $this->installationToken === null ? [] : ['X-Bunq-Client-Authentication' => [$this->installationToken]];
                $response = Http::send($this->config, new Wirespec\RawRequest(
                    method: $request->method,
                    path: $request->path,
                    queries: $request->queries,
                    headers: [...$request->headers, ...$headers],
                    body: $request->body,
                ));
                return $this->serverPublicKey === null
                    ? Http::requireTyped($response)
                    : Http::requireSigned($response, $this->serverPublicKey);
            }
        });
    }

    private static function setupFailure(string $what, Wirespec\Response $response): string
    {
        return \sprintf('%s (status %d): %s', $what, $response->status, $response->body->Error[0]->error_description ?? 'no error description');
    }

    /** Sessions can be for various types of users, of which only one is filled. */
    private static function userId(SessionServerCreate $session): int
    {
        return $session->UserPerson?->id
            ?? $session->UserCompany?->id
            ?? $session->UserApiKey?->id
            ?? $session->UserPaymentServiceProvider?->id
            ?? throw new \UnexpectedValueException('No user id found in the SessionServerCreate response');
    }

    private static function sessionTimeout(SessionServerCreate $session): int
    {
        $timeout = $session->UserPerson?->session_timeout
            ?? $session->UserCompany?->session_timeout
            ?? $session->UserPaymentServiceProvider?->session_timeout
            ?? self::anchoredUserSessionTimeout($session->UserApiKey?->granted_by_user)
            ?? self::anchoredUserSessionTimeout($session->UserApiKey?->requested_by_user);
        if ($timeout === null) {
            \error_log('bunq - No session timeout found in session server response, using default of 30 minutes');
        }
        return $timeout ?? self::DEFAULT_SESSION_TIMEOUT_SECONDS;
    }

    private static function anchoredUserSessionTimeout(?UserApiKeyAnchoredUser $user): ?int
    {
        return $user?->UserPerson?->session_timeout ?? $user?->UserCompany?->session_timeout ?? $user?->UserPaymentServiceProvider?->session_timeout;
    }
}
