<?php

declare(strict_types=1);

namespace Bunq\Sdk;

use Bunq\Api\Wirespec;

/**
 * Sends a raw request to bunq with curl and checks what comes back.
 */
final class Http
{
    /**
     * Sends the request to the config's server with the User-Agent header and, for a request with a body,
     * the `X-Bunq-Client-Signature` over that body. Response header names are lower case.
     */
    public static function send(Config $config, Wirespec\RawRequest $request): Wirespec\RawResponse
    {
        $query = \implode('&', \array_merge([], ...\array_map(
            static fn (string $key, array $values): array => \array_map(static fn (string $value): string => \rawurlencode($key) . '=' . \rawurlencode($value), $values),
            \array_keys($request->queries),
            \array_values($request->queries),
        )));
        $url = $config->bunqServer->baseUrl . \implode('/', \array_map(\rawurlencode(...), $request->path)) . ($query === '' ? '' : "?$query");

        $headers = \array_merge([], ...\array_map(
            static fn (string $key, array $values): array => \array_map(
                static fn (string $value): string => "$key: $value",
                \array_filter($values, static fn (string $value): bool => \trim($value) !== ''),
            ),
            \array_keys($request->headers),
            \array_values($request->headers),
        ));
        $headers[] = 'User-Agent: ' . (\trim($config->userAgent ?? '') ?: $config->serviceName);
        if ($request->body !== null) {
            $headers[] = 'X-Bunq-Client-Signature: ' . Signing::signData($config, $request->body);
        }

        $responseHeaders = [];
        $curl = \curl_init($url);
        \curl_setopt_array($curl, [
            \CURLOPT_CUSTOMREQUEST => $request->method,
            \CURLOPT_HTTPHEADER => $headers,
            \CURLOPT_RETURNTRANSFER => true,
            \CURLOPT_HEADERFUNCTION => static function (\CurlHandle $curl, string $line) use (&$responseHeaders): int {
                if (\str_contains($line, ':')) {
                    [$name, $value] = \explode(':', $line, 2);
                    $responseHeaders[\strtolower(\trim($name))][] = \trim($value);
                }
                return \strlen($line);
            },
        ]);
        if ($request->body !== null) {
            \curl_setopt($curl, \CURLOPT_POSTFIELDS, $request->body);
        }
        if ($config->connectTimeout !== null) {
            \curl_setopt($curl, \CURLOPT_CONNECTTIMEOUT_MS, (int) \ceil($config->connectTimeout * 1000));
        }
        if ($config->requestTimeout !== null) {
            \curl_setopt($curl, \CURLOPT_TIMEOUT_MS, (int) \ceil($config->requestTimeout * 1000));
        }
        $body = \curl_exec($curl);
        if ($body === false) {
            throw new \RuntimeException("Request to $url failed: " . \curl_error($curl));
        }
        $status = \curl_getinfo($curl, \CURLINFO_RESPONSE_CODE);

        return new Wirespec\RawResponse(statusCode: $status, headers: $responseHeaders, body: $body === '' ? null : $body);
    }

    /**
     * Only a 200 with a `Response` object or a 400 with an `Error` object is for the generated client.
     *
     * @throws BunqApiError for anything else
     */
    public static function requireTyped(Wirespec\RawResponse $response): Wirespec\RawResponse
    {
        $envelope = [200 => 'Response', 400 => 'Error'][$response->statusCode] ?? null;
        $document = \json_decode($response->body ?? '', true);
        return $envelope !== null && \is_array($document) && \array_key_exists($envelope, $document)
            ? $response
            : throw new BunqApiError($response->statusCode, $response->body ?? '', \array_change_key_case($response->headers));
    }

    /**
     * Like requireTyped, and the body must carry a valid `X-Bunq-Server-Signature` for the server public key.
     *
     * @throws \UnexpectedValueException when the signature is missing or invalid
     */
    public static function requireSigned(Wirespec\RawResponse $response, string $serverPublicKey): Wirespec\RawResponse
    {
        self::requireTyped($response);
        $signature = \array_change_key_case($response->headers)['x-bunq-server-signature'][0] ?? null;
        return Signing::verifyResponse($serverPublicKey, $response->body ?? '', $signature)
            ? $response
            : throw new \UnexpectedValueException('Invalid bunq server signature');
    }
}
