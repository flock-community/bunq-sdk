import base64
import unittest
from typing import Callable, Type

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec, rsa

from signing_keys import (
    InvalidPemFormatError,
    InvalidRsaKeyError,
    KeyMismatchError,
    KeyType,
    SigningKeyValidationError,
    SigningKeysFromPem,
    ValidationStage,
)


class Generated:
    def __init__(self) -> None:
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        pub = key.public_key()
        self.private_pem = key.private_bytes(
            serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()).decode()
        self.public_pem = pub.public_bytes(
            serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo).decode()
        self.pkcs1_private_pem = key.private_bytes(
            serialization.Encoding.PEM, serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption()).decode()
        self.pkcs1_public_pem = pub.public_bytes(
            serialization.Encoding.PEM, serialization.PublicFormat.PKCS1).decode()


def pem(block_type: str, der: bytes) -> str:
    return f"-----BEGIN {block_type}-----\n{base64.encodebytes(der).decode()}-----END {block_type}-----\n"


class SigningKeyValidationTest(unittest.TestCase):
    valid = Generated()

    def assert_failure(self, error_class: Type[SigningKeyValidationError], key_type: KeyType,
                       stage: ValidationStage, phrase: str, block: Callable[[], object]) -> None:
        with self.assertRaises(error_class) as context:
            block()
        e = context.exception
        self.assertEqual(key_type, e.key_type)
        self.assertEqual(stage, e.stage)
        self.assertIn(phrase, str(e))
        print(f"MESSAGE[{phrase}]: {e}")

    def test_pkcs1_private_key_gets_openssl_conversion_command(self) -> None:
        pkcs1 = self.valid.pkcs1_private_pem
        self.assert_failure(
            InvalidPemFormatError, KeyType.PRIVATE, ValidationStage.PEM_PARSING,
            "Private key validation failed during PEM parsing: the key is in PKCS#1 format",
            lambda: SigningKeysFromPem(pkcs1, self.valid.public_pem))
        self.assert_failure(
            InvalidPemFormatError, KeyType.PRIVATE, ValidationStage.PEM_PARSING,
            "openssl pkcs8 -topk8 -inform PEM -outform PEM -nocrypt -in private_key.pem -out private_key_pkcs8.pem",
            lambda: SigningKeysFromPem(pkcs1, self.valid.public_pem))

    def test_encrypted_private_key_is_rejected(self) -> None:
        encrypted = pem("ENCRYPTED PRIVATE KEY", b"0123456789")
        self.assert_failure(
            InvalidPemFormatError, KeyType.PRIVATE, ValidationStage.PEM_PARSING,
            "the command asks for the passphrase", lambda: SigningKeysFromPem(encrypted, self.valid.public_pem))

    def test_truncated_pem_reports_missing_end_line(self) -> None:
        truncated = self.valid.private_pem.split("-----END")[0]
        self.assert_failure(
            InvalidPemFormatError, KeyType.PRIVATE, ValidationStage.PEM_PARSING,
            "looks truncated", lambda: SigningKeysFromPem(truncated, self.valid.public_pem))

    def test_invalid_base64_body_is_rejected(self) -> None:
        bad = "-----BEGIN PUBLIC KEY-----\n!!!not base64!!!\n-----END PUBLIC KEY-----\n"
        self.assert_failure(
            InvalidPemFormatError, KeyType.PUBLIC, ValidationStage.PEM_PARSING,
            "not valid base64", lambda: SigningKeysFromPem(self.valid.private_pem, bad))

    def test_ec_private_key_is_rejected_as_non_rsa(self) -> None:
        ec_pem = ec.generate_private_key(ec.SECP256R1()).private_bytes(
            serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()).decode()
        self.assert_failure(
            InvalidRsaKeyError, KeyType.PRIVATE, ValidationStage.RSA_VALIDATION,
            "Private key validation failed during RSA validation",
            lambda: SigningKeysFromPem(ec_pem, self.valid.public_pem))

    def test_mismatched_key_pair_is_reported_for_both_keys(self) -> None:
        other = Generated()
        self.assert_failure(
            KeyMismatchError, KeyType.BOTH, ValidationStage.COMPATIBILITY_CHECK,
            "Private and public key validation failed during compatibility check",
            lambda: SigningKeysFromPem(self.valid.private_pem, other.public_pem))

    def test_literal_backslash_n_is_detected(self) -> None:
        env_var = self.valid.private_pem.strip().replace("\n", "\\n")
        self.assert_failure(
            InvalidPemFormatError, KeyType.PRIVATE, ValidationStage.PEM_PARSING,
            "literal \\n sequences", lambda: SigningKeysFromPem(env_var, self.valid.public_pem))

    def test_single_line_pem_is_detected(self) -> None:
        one_line = self.valid.public_pem.strip().replace("\n", " ")
        self.assert_failure(
            InvalidPemFormatError, KeyType.PUBLIC, ValidationStage.PEM_PARSING,
            "no line breaks", lambda: SigningKeysFromPem(self.valid.private_pem, one_line))

    def test_certificate_before_the_key_is_reported_as_wrong_block(self) -> None:
        cert = pem("CERTIFICATE", bytes([1, 2, 3])) + self.valid.public_pem
        self.assert_failure(
            InvalidPemFormatError, KeyType.PUBLIC, ValidationStage.PEM_PARSING,
            "the first PEM block is 'CERTIFICATE'", lambda: SigningKeysFromPem(self.valid.private_pem, cert))

    def test_pkcs1_public_key_gets_conversion_command(self) -> None:
        self.assert_failure(
            InvalidPemFormatError, KeyType.PUBLIC, ValidationStage.PEM_PARSING,
            "openssl rsa -RSAPublicKey_in -in public_key.pem -pubout -out public_key_spki.pem",
            lambda: SigningKeysFromPem(self.valid.private_pem, self.valid.pkcs1_public_pem))

    def test_public_key_passed_as_private_key(self) -> None:
        self.assert_failure(
            InvalidPemFormatError, KeyType.PRIVATE, ValidationStage.PEM_PARSING,
            "may be swapped", lambda: SigningKeysFromPem(self.valid.public_pem, self.valid.public_pem))

    def test_private_key_passed_as_public_key(self) -> None:
        self.assert_failure(
            InvalidPemFormatError, KeyType.PUBLIC, ValidationStage.PEM_PARSING,
            "may be swapped", lambda: SigningKeysFromPem(self.valid.private_pem, self.valid.private_pem))

    def test_cr_only_line_endings_load(self) -> None:
        SigningKeysFromPem(self.valid.private_pem.replace("\n", "\r"), self.valid.public_pem)

    def test_trailing_spaces_load(self) -> None:
        spaced = "\n".join(line + "   " for line in self.valid.private_pem.split("\n"))
        SigningKeysFromPem(spaced, self.valid.public_pem)

    def test_indented_pem_loads(self) -> None:
        indented = "\n".join("    " + line for line in self.valid.public_pem.split("\n"))
        SigningKeysFromPem(self.valid.private_pem, indented)

    def test_concatenated_private_and_public_pem_uses_the_first_block(self) -> None:
        SigningKeysFromPem(self.valid.private_pem + self.valid.public_pem, self.valid.public_pem)

    def test_dropped_body_line_mentions_truncated_or_corrupted(self) -> None:
        lines = self.valid.private_pem.split("\n")
        del lines[2]
        self.assert_failure(
            InvalidRsaKeyError, KeyType.PRIVATE, ValidationStage.RSA_VALIDATION,
            "may be truncated or corrupted", lambda: SigningKeysFromPem("\n".join(lines), self.valid.public_pem))


if __name__ == "__main__":
    unittest.main()
