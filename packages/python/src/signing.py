import hashlib
from typing import Optional

from cryptography.hazmat.primitives import hashes
import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from signing_keys import _validate_and_load_public_key


class Signing:

    @staticmethod
    def sign_data(config, data):
        private_key = config.signing_keys.private_key()

        # Ensure the data is encoded in UTF-8 exactly as it will be sent
        encoded_data = data.encode('utf-8')

        # Debug: Print exact bytes being signed
        # print(encoded_data)
        # print(private_key)
        # print("\n[DEBUG] Signing Data Bytes:", encoded_data)
        # print("[DEBUG] SHA256 Hash of Data:", hashlib.sha256(encoded_data).hexdigest())

        # Generate signature using SHA256 and PKCS#1 v1.5 padding as required by Bunq
        signature = private_key.sign(
            encoded_data,
            padding.PKCS1v15(),
            hashes.SHA256()
        )

        # Encode in Base64 (as required by Bunq API)
        encoded_signature = base64.b64encode(signature).decode('utf-8')

        # Debug: Print signature
        # print("[DEBUG] Base64 Encoded Signature:", encoded_signature)

        return encoded_signature

    @staticmethod
    def verify_response(server_public_key_pem: str, response_body: bytes, signature: Optional[str]) -> bool:
        """Verifies bunq's X-Bunq-Server-Signature: SHA256withRSA over the raw response body bytes.

        Returns True if the signature is valid, False otherwise (including a missing signature).
        """
        try:
            if not signature:
                return False
            _validate_and_load_public_key(server_public_key_pem).verify(
                base64.b64decode(signature, validate=True),
                response_body,
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            return True
        except Exception as e:
            print(f"[ERROR] Signature verification failed: {e}")
            return False
