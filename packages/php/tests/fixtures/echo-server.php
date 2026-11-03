<?php

declare(strict_types=1);

// Router for PHP's built-in server: answers every request with the method, URI, lower-cased headers and body it received.
\header('Content-Type: application/json');
echo \json_encode([
    'method' => $_SERVER['REQUEST_METHOD'],
    'uri' => $_SERVER['REQUEST_URI'],
    'headers' => \array_change_key_case(\getallheaders()),
    'body' => \file_get_contents('php://input'),
]);
