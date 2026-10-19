import json
import threading
import unittest
from dataclasses import replace
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Optional

from api.wirespec import Wirespec
from bunq_server import BunqServer
from bunq_signing_keys_generator import BunqSigningKeysGenerator
from config import create_config
from context import Context, init_context, refresh_session
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

    async def test_400_with_an_invalid_signature_raises(self):
        with self.assertRaisesRegex(Exception, "Invalid bunq server signature"):
            await self.call(400, '{"Error":[{"error_description":"x"}]}', sign_body(b"other"))

    async def test_400_with_a_missing_signature_raises(self):
        with self.assertRaisesRegex(Exception, "Invalid bunq server signature"):
            await self.call(400, '{"Error":[{"error_description":"x"}]}', None)

    async def test_signature_over_another_body_raises(self):
        with self.assertRaisesRegex(Exception, "Invalid bunq server signature"):
            await self.call(200, BODY, sign_body(b"other"))

    async def test_missing_signature_raises(self):
        with self.assertRaisesRegex(Exception, "Invalid bunq server signature"):
            await self.call(200, BODY, None)

    async def test_signature_that_is_not_base64_raises(self):
        with self.assertRaisesRegex(Exception, "Invalid bunq server signature"):
            await self.call(200, BODY, "not base64!")

    def unsigned_server_context(self, install_body: str) -> Context:
        """A context for a server that answers every POST unsigned: install_body for the installation, a session otherwise."""
        session = json.dumps({"Response": [{"Id": {"id": 1}}, {"Token": {"token": "t"}}, {"UserApiKey": {"id": 2}}]})

        class Handler(BaseHTTPRequestHandler):
            def do_POST(handler):
                handler.rfile.read(int(handler.headers.get('Content-Length', 0)))
                respond(handler, 200, (install_body if handler.path.endswith('installation') else session).encode(), None)

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
        return Context(SERVER_PUBLIC_KEY, 1, 1, 'token', 1, datetime.now() + timedelta(hours=1), 'installation', config)

    async def test_refresh_session_with_an_empty_server_public_key_raises(self):
        context = self.unsigned_server_context('{}')
        with self.assertRaisesRegex(Exception, "Invalid bunq server signature"):
            await refresh_session(replace(context, server_public_key=""))

    async def test_init_context_raises_on_an_unsigned_device_server_response(self):
        installation = json.dumps({"Response": [{"Id": {"id": 1}}, {"Token": {"token": "t"}},
                                                {"ServerPublicKey": {"server_public_key": SERVER_PUBLIC_KEY}}]})
        context = self.unsigned_server_context(installation)
        with self.assertRaisesRegex(Exception, "Invalid bunq server signature"):
            await init_context(context.config)

    def test_verify_response_checks_the_raw_body_bytes(self):
        body = b'{"a": 1}\n'
        signature = sign_body(body)
        self.assertTrue(Signing.verify_response(SERVER_PUBLIC_KEY, body, signature))
        self.assertFalse(Signing.verify_response(SERVER_PUBLIC_KEY, b'{"a":1}', signature))
        self.assertFalse(Signing.verify_response(SERVER_PUBLIC_KEY, body, None))


if __name__ == '__main__':
    unittest.main()
