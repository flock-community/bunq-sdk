"""Stands in for bunq's server key: local test servers sign their responses with it."""
import base64
from http.server import BaseHTTPRequestHandler
from typing import Optional

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from bunq_signing_keys_generator import BunqSigningKeysGenerator
from signing_keys import SigningKeysFromPem

_private_key_pem, SERVER_PUBLIC_KEY = BunqSigningKeysGenerator.generate_bunq_signing_keys_as_pem()
_keys = SigningKeysFromPem(_private_key_pem, SERVER_PUBLIC_KEY)


def sign_body(body: bytes) -> str:
    return base64.b64encode(_keys.private_key().sign(body, padding.PKCS1v15(), hashes.SHA256())).decode('utf-8')


def respond(handler: BaseHTTPRequestHandler, status: int, body: bytes, signature: Optional[str] = "valid") -> None:
    """Answers with body and an X-Bunq-Server-Signature header: valid by default, none when signature is None."""
    handler.send_response(status)
    if signature is not None:
        handler.send_header('X-Bunq-Server-Signature', sign_body(body) if signature == "valid" else signature)
    handler.send_header('Content-Length', str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)
