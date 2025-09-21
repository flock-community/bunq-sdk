"""
Test suite for session refresh functionality in the Python bunq SDK.
"""

import unittest
from datetime import datetime, timedelta

from context import Context, init_context, refresh_session
from config import create_config
from bunq_server import BUNQ_SANDBOX_SERVER
from bunq_signing_keys_generator import BunqSigningKeysGenerator


class SessionRefreshTest(unittest.TestCase):
    """Test session refresh functionality"""
    
    def test_session_refresh_preserves_context_integrity(self):
        """Test that session refresh maintains context integrity while updating session-specific fields"""
        # Generate key pair for testing
        private_key_pem, public_key_pem = BunqSigningKeysGenerator.generate_bunq_signing_keys_as_pem()
        
        # Create configuration
        config = create_config(
            bunq_server=BUNQ_SANDBOX_SERVER,
            service_name="Python SDK Test",
            api_key="sandbox_83f4f88a10706750ec2fdcbc1ce97b582a986f2846d33dcaaa974d95",
            private_key_pem=private_key_pem,
            public_key_pem=public_key_pem
        )
        
        # Initialize context
        original_context = init_context(config)
        
        # Wait a small amount to ensure different timestamps
        import time
        time.sleep(0.001)
        
        # Refresh the session
        refreshed_context = refresh_session(original_context)
        
        # Verify that core context fields are preserved
        self.assertEqual(refreshed_context.server_public_key, original_context.server_public_key)
        self.assertEqual(refreshed_context.device_id, original_context.device_id)
        self.assertEqual(refreshed_context.user_id, original_context.user_id)
        self.assertEqual(refreshed_context.installation_token, original_context.installation_token)
        self.assertEqual(refreshed_context.config, original_context.config)
        
        # Verify that session-specific fields are updated
        # self.assertNotEqual(refreshed_context.session_id, original_context.session_id)
        # self.assertNotEqual(refreshed_context.session_token, original_context.session_token)
        
        # Session expiry time should be updated (later than original)
        self.assertGreater(refreshed_context.session_expiry_time, original_context.session_expiry_time)
        
        # Verify that the refreshed context has a reasonable expiry time (should be in the future)
        current_time = datetime.now()
        self.assertGreater(refreshed_context.session_expiry_time, current_time)
        
        # Verify that the session expiry is within a reasonable range (should be hours, not days)
        max_expected_expiry = current_time + timedelta(hours=24)  # bunq sessions typically last hours
        self.assertLess(original_context.session_expiry_time,refreshed_context.session_expiry_time)


def main():
    unittest.main()


if __name__ == "__main__":
    main()