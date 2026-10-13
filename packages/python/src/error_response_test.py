import threading
import unittest
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

from api.endpoint.ReadUser import Response200, Response400, ReadUser
from api.wirespec import Wirespec
from bunq_server import BunqServer
from bunq_signing_keys_generator import BunqSigningKeysGenerator
from config import create_config
from context import Context
from transport import BunqApiError, Serialization
from wirespec import bunq_client


class ErrorResponseTest(unittest.IsolatedAsyncioTestCase):

    def read_user(self, status: int, body: str):
        return ReadUser.fromRawResponse(Serialization(), Wirespec.RawResponse(status, {}, body.encode('utf-8')))

    async def read_user_answering(self, status: int, body: str):
        class Handler(BaseHTTPRequestHandler):
            def do_GET(handler):
                content = body.encode('utf-8')
                handler.send_response(status)
                handler.send_header('Content-Length', str(len(content)))
                handler.end_headers()
                handler.wfile.write(content)

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
        context = Context('', 1, 1, 'token', 1, datetime.now(), 'installation', config)
        return await bunq_client(context).read_user(1)

    async def test_400_error_body_without_response_envelope_is_a_typed_response_400(self):
        response = await self.read_user_answering(
            400, '{"Error":[{"error_description":"Missing required field \\"currency\\"."}]}')

        self.assertIsInstance(response, Response400)
        self.assertEqual('Missing required field "currency".', response.body.Error[0].error_description)

    def test_body_without_response_or_error_is_rejected(self):
        with self.assertRaises(Exception):
            self.read_user(200, '{"unexpected":true}')

    async def test_status_other_than_200_and_400_raises_with_status_and_body(self):
        for status in (403, 404, 500):
            body = '{"Error":[{"error_description":"nope %d"}]}' % status
            with self.assertRaises(BunqApiError) as raised:
                await self.read_user_answering(status, body)

            self.assertEqual(status, raised.exception.status)
            self.assertEqual(body, raised.exception.body)

    async def test_html_500_raises_with_the_html_as_body(self):
        with self.assertRaises(BunqApiError) as raised:
            await self.read_user_answering(500, '<html>Internal Server Error</html>')

        self.assertEqual(500, raised.exception.status)
        self.assertEqual('<html>Internal Server Error</html>', raised.exception.body)

    async def test_400_that_is_not_json_raises(self):
        with self.assertRaises(BunqApiError) as raised:
            await self.read_user_answering(400, '<html>Bad Request</html>')

        self.assertEqual(400, raised.exception.status)

    def test_message_truncates_the_body_but_the_body_field_keeps_it_whole(self):
        error = BunqApiError(502, 'x' * 2000)

        self.assertLess(len(str(error)), 600)
        self.assertEqual(2000, len(error.body))

    async def test_200_is_returned_as_is(self):
        response = await self.read_user_answering(200, '{"Response":[{"UserPerson":{"id":1}}]}')

        self.assertIsInstance(response, Response200)


if __name__ == '__main__':
    unittest.main()
