import asyncio
import json
import threading
import unittest
from dataclasses import replace
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from api.wirespec import Wirespec
from bunq_server import BunqServer
from bunq_signing_keys_generator import BunqSigningKeysGenerator
from config import create_config
from context import Context
from datetime import datetime
from transport import BunqApiError
from wirespec import transportation

SESSION_REJECTED = json.dumps({"Error": [{"error_description": "Insufficient authentication."}]})
NOT_ALLOWED = json.dumps({"Error": [{"error_description": "You are not allowed to do this."}]})


class RefreshTest(unittest.IsolatedAsyncioTestCase):

    def start_server(self, rejected_body: str):
        """Answers 200 for the 'fresh' token and a 403 with rejected_body for every other token."""
        self.tokens_seen: list[str | None] = []

        class Handler(BaseHTTPRequestHandler):
            def do_GET(handler):
                token = handler.headers.get('X-Bunq-Client-Authentication')
                self.tokens_seen.append(token)
                ok = token == 'fresh'
                body = b'{"Response":[]}' if ok else rejected_body.encode()
                handler.send_response(200 if ok else 403)
                handler.send_header('Content-Length', str(len(body)))
                handler.end_headers()
                handler.wfile.write(body)

            def log_message(handler, *args):
                pass

        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
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
        self.context = Context('', 1, 1, 'stale', 1, datetime.now(), 'installation', config)

    def counting_refresh(self, fails: bool = False):
        self.refreshes = 0

        async def refresh(context: Context) -> Context:
            self.refreshes += 1
            await asyncio.sleep(0.05)
            if fails:
                raise Exception("refresh failed")
            return replace(context, session_token='fresh')

        return refresh

    request = Wirespec.RawRequest('GET', ['ping'], {}, {}, None)

    async def test_session_rejected_refreshes_once_and_retries_with_new_token(self):
        self.start_server(SESSION_REJECTED)
        response = await transportation(self.context, self.counting_refresh()).transport(self.request)

        self.assertEqual(200, response.statusCode)
        self.assertEqual(1, self.refreshes)
        self.assertEqual(['stale', 'fresh'], self.tokens_seen)

    async def test_failed_refresh_raises_original_403(self):
        self.start_server(SESSION_REJECTED)
        with self.assertRaises(BunqApiError) as raised:
            await transportation(self.context, self.counting_refresh(fails=True)).transport(self.request)

        self.assertEqual(403, raised.exception.status)
        self.assertEqual(SESSION_REJECTED, raised.exception.body)
        self.assertEqual(1, self.refreshes)

    async def test_cancelled_refresh_propagates(self):
        self.start_server(SESSION_REJECTED)

        async def cancelled_refresh(context: Context) -> Context:
            raise asyncio.CancelledError()

        with self.assertRaises(asyncio.CancelledError):
            await transportation(self.context, cancelled_refresh).transport(self.request)

    async def test_other_403_does_not_refresh(self):
        self.start_server(NOT_ALLOWED)
        with self.assertRaises(BunqApiError) as raised:
            await transportation(self.context, self.counting_refresh()).transport(self.request)

        self.assertEqual(403, raised.exception.status)
        self.assertEqual(0, self.refreshes)

    async def test_empty_403_does_not_refresh(self):
        self.start_server('')
        with self.assertRaises(BunqApiError) as raised:
            await transportation(self.context, self.counting_refresh()).transport(self.request)

        self.assertEqual(403, raised.exception.status)
        self.assertEqual(0, self.refreshes)

    async def test_html_403_raises_and_does_not_refresh(self):
        self.start_server('<html>forbidden</html>')
        with self.assertRaises(BunqApiError) as raised:
            await transportation(self.context, self.counting_refresh()).transport(self.request)

        self.assertEqual(403, raised.exception.status)
        self.assertEqual('<html>forbidden</html>', raised.exception.body)
        self.assertEqual(0, self.refreshes)

    async def test_concurrent_rejections_share_one_refresh(self):
        self.start_server(SESSION_REJECTED)
        transport = transportation(self.context, self.counting_refresh())
        responses = await asyncio.gather(*[transport.transport(self.request) for _ in range(5)])

        self.assertEqual([200] * 5, [response.statusCode for response in responses])
        self.assertEqual(1, self.refreshes)

    async def test_later_requests_use_the_refreshed_token(self):
        self.start_server(SESSION_REJECTED)
        transport = transportation(self.context, self.counting_refresh())
        await transport.transport(self.request)
        self.tokens_seen.clear()
        await transport.transport(self.request)

        self.assertEqual(['fresh'], self.tokens_seen)
        self.assertEqual(1, self.refreshes)


if __name__ == '__main__':
    unittest.main()
