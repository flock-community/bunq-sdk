<?php

declare(strict_types=1);

// Router for PHP's built-in server: answers every request with the method, URI, lower-cased headers and body it received.
// A `delay` query parameter (milliseconds) makes it wait before answering, to test timeouts.
\usleep(1000 * (int) ($_GET['delay'] ?? 0));
\header('Content-Type: application/json');
echo \json_encode([
    'method' => $_SERVER['REQUEST_METHOD'],
    'uri' => $_SERVER['REQUEST_URI'],
    'headers' => \array_change_key_case(\getallheaders()),
    'body' => \file_get_contents('php://input'),
]);
