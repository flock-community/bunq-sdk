import threading
import unittest
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Optional

from api.wirespec import Wirespec
from bunq_server import BunqServer
from bunq_signing_keys_generator import BunqSigningKeysGenerator
from config import create_config
from context import Context
from server_key import SERVER_PUBLIC_KEY, respond, sign_body
from signing import Signing
from wirespec import transportation

BODY = '{"Response":[]}'


class ResponseSignatureTest(unittest.IsolatedAsyncioTestCase):

    async def call(self, status: int, body: str, signature: Optional[str]) -> Wirespec.RawResponse:
        class Handler(BaseHTTPRequestHandler):
            def do_GET(handler):
                respond(handler, status, body.encode('utf-8'), signature)

            def log_message(handler, *args):
                pass

        server = HTTPServer(('127.0.0.1', 0), Handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        private_key_pem, public_key_pem = BunqSigningKeysGenerator.generate_bunq_signing_keys_as_pem()
        config = create_config(
            bunq_server=BunqServer(f'http://127.0.0.1:{server.server_port}/', ''),
            service_name='my-service',
            api_key='key',
            private_key_pem=private_key_pem,
            public_key_pem=public_key_pem)
        context = Context(SERVER_PUBLIC_KEY, 1, 1, 'token', 1, datetime.now() + timedelta(hours=1), 'installation', config)
        return await transportation(context).transport(Wirespec.RawRequest('GET', ['ping'], {}, {}, None))

    async def test_valid_signature_passes(self):
        self.assertEqual(200, (await self.call(200, BODY, "valid")).statusCode)

    async def test_valid_signature_on_a_400_passes(self):
        self.assertEqual(400, (await self.call(400, '{"Error":[{"error_description":"x"}]}', "valid")).statusCode)

    async def test_signature_over_another_body_raises(self):
        with self.assertRaisesRegex(Exception, "Invalid bunq server signature"):
            await self.call(200, BODY, sign_body(b"other"))

    async def test_missing_signature_raises(self):
        with self.assertRaisesRegex(Exception, "Invalid bunq server signature"):
            await self.call(200, BODY, None)

    async def test_signature_that_is_not_base64_raises(self):
        with self.assertRaisesRegex(Exception, "Invalid bunq server signature"):
            await self.call(200, BODY, "not base64!")

    def test_verify_response_checks_the_raw_body_bytes(self):
        body = b'{"a": 1}\n'
        signature = sign_body(body)
        self.assertTrue(Signing.verify_response(SERVER_PUBLIC_KEY, body, signature))
        self.assertFalse(Signing.verify_response(SERVER_PUBLIC_KEY, b'{"a":1}', signature))
        self.assertFalse(Signing.verify_response(SERVER_PUBLIC_KEY, body, None))


if __name__ == '__main__':
    unittest.main()
