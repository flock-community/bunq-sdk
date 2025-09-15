import hashlib

from cryptography.hazmat.primitives import hashes
import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


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

    def verify_response(response_body, signature, server_public_key_pem):
        """Verifies the server's response signature.

        Args:
            response_body (str): The response body as a string
            signature (str): The base64 encoded signature from X-Bunq-Server-Signature header
            server_public_key_pem (str): The server's public key in PEM format

        Returns:
            bool: True if signature is valid, False otherwise
        """
        try:
            # Load the server's public key
            public_key = load_public_key(server_public_key_pem)

            # Decode the base64 signature
            decoded_signature = base64.b64decode(signature)

            # Verify the signature
            public_key.verify(
                decoded_signature,
                response_body.encode('utf-8'),
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            return True
        except Exception as e:
            print(f"[ERROR] Signature verification failed: {e}")
            return False
