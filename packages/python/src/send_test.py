import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer

import httpx

from bunq_server import BunqServer
from bunq_signing_keys_generator import BunqSigningKeysGenerator
from config import create_config
from transport import send, timeout_for
from api.wirespec import Wirespec


class SendTest(unittest.IsolatedAsyncioTestCase):

    async def received_for(self, request: Wirespec.RawRequest):
        received = []

        class Handler(BaseHTTPRequestHandler):
            def handle_request(self):
                received.append((self.path, self.headers.get('X-Bunq-Client-Signature')))
                self.send_response(200)
                self.send_header('Content-Length', '0')
                self.end_headers()

            do_GET = do_POST = handle_request

            def log_message(self, *args):
                pass

        server = HTTPServer(('127.0.0.1', 0), Handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            private_key_pem, public_key_pem = BunqSigningKeysGenerator.generate_bunq_signing_keys_as_pem()
            config = create_config(
                bunq_server=BunqServer(f'http://127.0.0.1:{server.server_port}/', ''),
                service_name='my-service',
                api_key='key',
                private_key_pem=private_key_pem,
                public_key_pem=public_key_pem)
            await send(config, request)
        finally:
            server.shutdown()
            server.server_close()
        return received

    async def test_sends_query_and_signs_request_with_body(self):
        [(path, signature)] = await self.received_for(
            Wirespec.RawRequest('POST', ['ping'], {'count': ['10']}, {}, b'{}'))

        self.assertEqual('/ping?count=10', path)
        self.assertTrue(signature)

    async def test_request_without_an_answer_within_the_request_timeout_raises_timeout_exception(self):
        release = threading.Event()

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                release.wait(10)

            def log_message(self, *args):
                pass

        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            config = self.config(server.server_port, request_timeout=0.2)

            with self.assertRaises(httpx.TimeoutException):
                await send(config, Wirespec.RawRequest('GET', ['ping'], {}, {}, None))
        finally:
            release.set()
            server.shutdown()
            server.server_close()

    def test_timeouts_are_passed_to_httpx(self):
        config = self.config(1, connect_timeout=3.0, request_timeout=20.0)

        self.assertEqual(httpx.Timeout(20.0, connect=3.0), timeout_for(config))

    def test_unset_timeouts_keep_the_httpx_default(self):
        self.assertEqual(httpx.Timeout(5.0), timeout_for(self.config(1)))

    def config(self, port: int, **timeouts):
        private_key_pem, public_key_pem = BunqSigningKeysGenerator.generate_bunq_signing_keys_as_pem()
        return create_config(
            bunq_server=BunqServer(f'http://127.0.0.1:{port}/', ''),
            service_name='my-service',
            api_key='key',
            private_key_pem=private_key_pem,
            public_key_pem=public_key_pem,
            **timeouts)

    async def test_does_not_sign_request_without_body(self):
        [(_, signature)] = await self.received_for(Wirespec.RawRequest('GET', ['ping'], {}, {}, None))

        self.assertIsNone(signature)


if __name__ == '__main__':
    unittest.main()
