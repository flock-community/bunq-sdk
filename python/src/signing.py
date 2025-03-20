import os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key
import base64
import json
import hashlib


# Function to generate RSA key pair
def generate_rsa_key_pair():
    private_key_file = 'private_key.pem'
    public_key_file = 'public_key.pem'
    
    # Check if the key files exist
    if os.path.exists(private_key_file) and os.path.exists(public_key_file):
        # Read the existing keys from the text files
        with open(private_key_file, 'r') as private_file:
            private_key_pem = private_file.read()

        with open(public_key_file, 'r') as public_file:
            public_key_pem = public_file.read()

        print("bunq - using existing keypair")
    else:
        # Generate new RSA keys with 2048 bits as required by Bunq
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        # Serialize private key to PEM format (PKCS#8 as required by Bunq)
        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode('utf-8')

        # Serialize public key to PEM format
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

        # Save the keys to text files
        with open(private_key_file, 'w') as private_file:
            private_file.write(private_key_pem)

        with open(public_key_file, 'w') as public_file:
            public_file.write(public_key_pem)

        print("bunq - creating new keypair [KEEP THESE FILES SAFE]")

    return private_key_pem, public_key_pem


def load_private_key(private_key_pem):
    """Load a private key from PEM format."""
    return load_pem_private_key(private_key_pem.encode(), password=None, backend=default_backend())


def load_public_key(public_key_pem):
    """Load a public key from PEM format."""
    return serialization.load_pem_public_key(
        public_key_pem.encode(),
        backend=default_backend()
    )


def sign_data(data, private_key_pem):
    """Signs the given data with the provided private key using SHA256 and PKCS#1 v1.5 padding.
    
    Args:
        data (str): The data to sign (should be the JSON request body)
        private_key_pem (str): The private key in PEM format
    
    Returns:
        str: Base64 encoded signature
    """
    private_key = load_private_key(private_key_pem)
    
    # Ensure the data is encoded in UTF-8 exactly as it will be sent
    encoded_data = data.encode('utf-8')

    # Debug: Print exact bytes being signed
    print("\n[DEBUG] Signing Data Bytes:", encoded_data)
    print("[DEBUG] SHA256 Hash of Data:", hashlib.sha256(encoded_data).hexdigest())

    # Generate signature using SHA256 and PKCS#1 v1.5 padding as required by Bunq
    signature = private_key.sign(
        encoded_data,
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    # Encode in Base64 (as required by Bunq API)
    encoded_signature = base64.b64encode(signature).decode('utf-8')

    # Debug: Print signature
    print("[DEBUG] Base64 Encoded Signature:", encoded_signature)

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

