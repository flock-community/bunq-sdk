import json
import threading
import unittest
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

from api.endpoint.ListAllMonetaryAccountBankForUser import Response200
from bunq_server import BunqServer
from bunq_signing_keys_generator import BunqSigningKeysGenerator
from config import create_config
from context import Context
from wirespec import bunq_client


class PaginationTest(unittest.IsolatedAsyncioTestCase):

    async def list_answering(self, body: dict):
        class Handler(BaseHTTPRequestHandler):
            def do_GET(handler):
                content = json.dumps(body).encode('utf-8')
                handler.send_response(200)
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
        return await bunq_client(context).list_all_monetary_account_bank_for_user(1, 2, None, None)

    async def test_list_response_keeps_the_items_and_the_pagination_block(self):
        response = await self.list_answering({
            "Response": [{"MonetaryAccountBank": {"id": 2, "description": "second"}},
                         {"MonetaryAccountBank": {"id": 1, "description": "first"}}],
            "Pagination": {"future_url": "/v1/future?newer_id=2", "newer_url": None,
                           "older_url": "/v1/older?older_id=1"},
        })

        self.assertIsInstance(response, Response200)
        self.assertEqual([2, 1], [item.id for item in response.body.Response])
        self.assertEqual("/v1/future?newer_id=2", response.body.Pagination.future_url)
        self.assertIsNone(response.body.Pagination.newer_url)
        self.assertEqual("/v1/older?older_id=1", response.body.Pagination.older_url)

    async def test_empty_page_has_an_empty_list_and_its_pagination(self):
        response = await self.list_answering({
            "Response": [],
            "Pagination": {"future_url": None, "newer_url": None, "older_url": None},
        })

        self.assertIsInstance(response, Response200)
        self.assertEqual([], response.body.Response)
        self.assertIsNone(response.body.Pagination.older_url)


if __name__ == "__main__":
    unittest.main()
