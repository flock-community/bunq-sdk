import unittest
from datetime import datetime

from bunq_server import BunqServer
from bunq_signing_keys_generator import BunqSigningKeysGenerator
from config import create_config
from context import Context


class SecretMaskingTest(unittest.TestCase):

    def test_repr_masks_secrets_and_keeps_non_secret_fields(self):
        private_key_pem, public_key_pem = BunqSigningKeysGenerator.generate_bunq_signing_keys_as_pem()
        config = create_config(BunqServer('http://localhost/', ''), 'my-service', 'secret-api-key',
                               private_key_pem, public_key_pem)
        context = Context('server-key', 1, 2, 'secret-session', 3, datetime(1970, 1, 1), 'secret-install', config)

        text = repr(context)

        for secret in ['secret-api-key', 'secret-session', 'secret-install', private_key_pem.splitlines()[1]]:
            self.assertNotIn(secret, text)
        self.assertIn('my-service', text)
        self.assertIn('user_id=3', text)


if __name__ == '__main__':
    unittest.main()
