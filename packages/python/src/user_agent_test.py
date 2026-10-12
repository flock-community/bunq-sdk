import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

from bunq_server import BunqServer
from bunq_signing_keys_generator import BunqSigningKeysGenerator
from config import create_config
from transport import send
from api.wirespec import Wirespec


class UserAgentTest(unittest.IsolatedAsyncioTestCase):

    async def user_agent_sent_for(self, **config_options):
        received = []

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                received.append(self.headers.get('User-Agent'))
                self.send_response(200)
                self.send_header('Content-Length', '0')
                self.end_headers()

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
                public_key_pem=public_key_pem,
                **config_options)
            await send(config, Wirespec.RawRequest('POST', ['ping'], {}, {}, b'{}'))
        finally:
            server.shutdown()
            server.server_close()
        return received

    async def test_defaults_to_service_name(self):
        self.assertEqual(['my-service'], await self.user_agent_sent_for())

    async def test_blank_user_agent_falls_back_to_service_name(self):
        self.assertEqual(['my-service'], await self.user_agent_sent_for(user_agent=''))

    async def test_uses_configured_user_agent(self):
        self.assertEqual(['my-agent'], await self.user_agent_sent_for(user_agent='my-agent'))


if __name__ == '__main__':
    unittest.main()
