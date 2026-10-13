import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

from bunq_server import BunqServer
from bunq_signing_keys_generator import BunqSigningKeysGenerator
from config import create_config
from transport import send
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

    async def test_does_not_sign_request_without_body(self):
        [(_, signature)] = await self.received_for(Wirespec.RawRequest('GET', ['ping'], {}, {}, None))

        self.assertIsNone(signature)


if __name__ == '__main__':
    unittest.main()
