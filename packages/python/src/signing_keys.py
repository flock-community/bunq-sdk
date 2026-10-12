"""
SigningKeys sealed hierarchy for RSA key pairs used in bunq API request signing.

Provides consistent access to both PEM string representations and parsed 
RSA key objects, ensuring they remain synchronized.
"""

import base64
import re
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Optional, Tuple
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


class ConfigValidationError(Exception):
    """Base exception for configuration validation errors"""
    def __init__(self, message: str, cause: Optional[Exception] = None):
        super().__init__(message)
        self.cause = cause


class KeyType(Enum):
    PRIVATE = "Private key"
    PUBLIC = "Public key"
    BOTH = "Private and public key"


class ValidationStage(Enum):
    PEM_PARSING = "PEM parsing"
    RSA_VALIDATION = "RSA validation"
    COMPATIBILITY_CHECK = "compatibility check"


class SigningKeyValidationError(ConfigValidationError):
    """Signing key validation failure: "<key> validation failed during <stage>: <detail>"."""
    def __init__(self, detail: str, key_type: KeyType, stage: ValidationStage,
                 cause: Optional[Exception] = None):
        super().__init__(f"{key_type.value} validation failed during {stage.value}: {detail}", cause)
        self.key_type = key_type
        self.stage = stage


class InvalidPemFormatError(SigningKeyValidationError):
    """Error thrown when PEM format validation fails"""
    def __init__(self, detail: str, key_type: KeyType, cause: Optional[Exception] = None):
        super().__init__(detail, key_type, ValidationStage.PEM_PARSING, cause)


class InvalidRsaKeyError(SigningKeyValidationError):
    """Error thrown when RSA key validation fails"""
    def __init__(self, detail: str, key_type: KeyType, cause: Optional[Exception] = None):
        super().__init__(detail, key_type, ValidationStage.RSA_VALIDATION, cause)


class KeyMismatchError(SigningKeyValidationError):
    """Error thrown when private and public keys don't match"""
    def __init__(self, detail: str):
        super().__init__(detail, KeyType.BOTH, ValidationStage.COMPATIBILITY_CHECK)


class SigningKeys(ABC):
    """
    Abstract base class for RSA key pairs used in bunq API request signing.
    
    Provides consistent access to both PEM string representations and parsed 
    RSA key objects, ensuring they remain synchronized.
    
    Available implementations:
    - SigningKeysFromPem - Load from PEM strings (most common)
    - SigningKeysFromRsa - Wrap existing RSA key objects
    """
    
    @abstractmethod
    def private_key_as_pem(self) -> str:
        """Get the private key as a PEM string"""
        pass
    
    @abstractmethod
    def public_key_as_pem(self) -> str:
        """Get the public key as a PEM string"""
        pass
    
    @abstractmethod
    def private_key(self) -> rsa.RSAPrivateKey:
        """Get the private key as an RSA object"""
        pass
    
    @abstractmethod
    def public_key(self) -> rsa.RSAPublicKey:
        """Get the public key as an RSA object"""
        pass


class SigningKeysFromPem(SigningKeys):
    """SigningKeys implementation that loads from PEM string representations"""
    
    def __init__(self, private_key_pem: str, public_key_pem: str):
        self._private_key_pem = private_key_pem
        self._public_key_pem = public_key_pem
        
        self._private_key_obj = _validate_and_load_private_key(private_key_pem)
        self._public_key_obj = _validate_and_load_public_key(public_key_pem)
        
        _validate_key_compatibility(self._private_key_obj, self._public_key_obj)
    
    def private_key_as_pem(self) -> str:
        return self._private_key_pem
    
    def public_key_as_pem(self) -> str:
        return self._public_key_pem
    
    def private_key(self) -> rsa.RSAPrivateKey:
        return self._private_key_obj
    
    def public_key(self) -> rsa.RSAPublicKey:
        return self._public_key_obj


class SigningKeysFromRsa(SigningKeys):
    """SigningKeys implementation that wraps existing RSA key objects"""
    
    def __init__(self, private_key: rsa.RSAPrivateKey, public_key: rsa.RSAPublicKey):
        self._private_key_obj = private_key
        self._public_key_obj = public_key
        
        _validate_key_compatibility(self._private_key_obj, self._public_key_obj)
        
        self._private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode('utf-8')
        
        self._public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')
    
    def private_key_as_pem(self) -> str:
        return self._private_key_pem
    
    def public_key_as_pem(self) -> str:
        return self._public_key_pem
    
    def private_key(self) -> rsa.RSAPrivateKey:
        return self._private_key_obj
    
    def public_key(self) -> rsa.RSAPublicKey:
        return self._public_key_obj


_PKCS8_FIX = "openssl pkcs8 -topk8 -inform PEM -outform PEM -nocrypt -in private_key.pem -out private_key_pkcs8.pem"
_PUBLIC_FROM_PRIVATE_FIX = "openssl rsa -in private_key_pkcs8.pem -pubout -out public_key.pem"
_BEGIN_LINE = re.compile(r"^-----BEGIN (.+)-----$")


def _validate_and_load_private_key(private_key_pem: str) -> rsa.RSAPrivateKey:
    """Validate and load a private key from PEM format"""
    der = _read_pem_body(private_key_pem, "PRIVATE KEY", KeyType.PRIVATE)
    hint = "Generate one with: openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048"
    try:
        key = serialization.load_der_private_key(der, password=None)
    except Exception as e:
        raise _not_rsa(str(e), KeyType.PRIVATE, hint, e)
    if not isinstance(key, rsa.RSAPrivateKey):
        raise _not_rsa(f"key type is {type(key).__name__}", KeyType.PRIVATE, hint)
    return key


def _validate_and_load_public_key(public_key_pem: str) -> rsa.RSAPublicKey:
    """Validate and load a public key from PEM format"""
    der = _read_pem_body(public_key_pem, "PUBLIC KEY", KeyType.PUBLIC)
    hint = f"Derive it with: {_PUBLIC_FROM_PRIVATE_FIX}"
    try:
        key = serialization.load_der_public_key(der)
    except Exception as e:
        raise _not_rsa(str(e), KeyType.PUBLIC, hint, e)
    if not isinstance(key, rsa.RSAPublicKey):
        raise _not_rsa(f"key type is {type(key).__name__}", KeyType.PUBLIC, hint)
    return key


def _not_rsa(reason: str, key_type: KeyType, hint: str, cause: Optional[Exception] = None) -> InvalidRsaKeyError:
    return InvalidRsaKeyError(
        f"not a valid RSA key ({reason}). The key may be truncated or corrupted, or not an RSA key "
        f"(only RSA keys are supported). {hint}",
        key_type, cause)


def _parse_first_pem_block(lines: List[str]) -> Optional[Tuple[str, List[str], bytes]]:
    begin = next((i for i, line in enumerate(lines) if _BEGIN_LINE.match(line)), None)
    if begin is None:
        return None
    match = _BEGIN_LINE.match(lines[begin])
    assert match is not None
    end = next((i for i in range(begin + 1, len(lines)) if lines[i] == f"-----END {match.group(1)}-----"), None)
    if end is None:
        return None
    body = lines[begin + 1:end]
    headers = [line for line in body if ":" in line]
    base64_body = "".join(line for line in body if ":" not in line)
    return match.group(1), headers, base64.b64decode(base64_body, validate=True)


def _read_pem_body(pem: str, label: str, key_type: KeyType) -> bytes:
    def invalid(detail: str, cause: Optional[Exception] = None) -> InvalidPemFormatError:
        return InvalidPemFormatError(detail, key_type, cause)

    if "\\n" in pem:
        raise invalid("the PEM contains literal \\n sequences; replace them with real newlines")
    lines = [line.strip() for line in re.split(r"\r\n|\r|\n", pem) if line.strip()]
    if len(lines) < 2:
        raise invalid("the PEM has no line breaks; put the BEGIN line, the base64 body and the END line on separate lines")
    begin_match = next((m for m in map(_BEGIN_LINE.match, lines) if m), None)
    if begin_match is not None:
        begin_index = lines.index(begin_match.group(0))
        if f"-----END {begin_match.group(1)}-----" not in lines[begin_index + 1:]:
            raise invalid(f"the '-----END {label}-----' line is missing, the PEM looks truncated")

    try:
        block = _parse_first_pem_block(lines)
    except Exception as e:
        raise invalid(f"the body is not valid base64 or is malformed ({e}). Re-export the key without modifying it.", e)
    if block is None:
        raise invalid("no PEM block could be read; check that the BEGIN line is present and the line breaks are real newlines")

    block_type, headers, content = block
    encrypted = block_type == "ENCRYPTED PRIVATE KEY" or any(
        h.startswith("Proc-Type:") and "ENCRYPTED" in h for h in headers)
    expects_private = key_type == KeyType.PRIVATE
    if block_type == label and not encrypted:
        return content
    if encrypted and expects_private:
        raise invalid(
            "the key is encrypted, which is not supported. Decrypt it first (the command asks for the passphrase): "
            "openssl pkcs8 -topk8 -nocrypt -in encrypted_key.pem -out private_key_pkcs8.pem")
    if block_type == "RSA PRIVATE KEY" and expects_private:
        raise invalid(f"the key is in PKCS#1 format but PKCS#8 ('-----BEGIN PRIVATE KEY-----') is required. Convert it with: {_PKCS8_FIX}")
    if block_type == "RSA PUBLIC KEY" and not expects_private:
        raise invalid(
            "the key is in PKCS#1 format but X.509 ('-----BEGIN PUBLIC KEY-----') is required. Convert it with: "
            "openssl rsa -RSAPublicKey_in -in public_key.pem -pubout -out public_key_spki.pem")
    if expects_private and block_type.endswith("PUBLIC KEY"):
        raise invalid("this is a public key, a private key is expected. The keys may be swapped.")
    if not expects_private and block_type.endswith("PRIVATE KEY"):
        raise invalid(
            "this is a private key, a public key is expected. The keys may be swapped. "
            f"Derive the public key with: {_PUBLIC_FROM_PRIVATE_FIX}")
    raise invalid(f"the first PEM block is '{block_type}' but '{label}' is expected")


def _validate_key_compatibility(private_key: rsa.RSAPrivateKey, public_key: rsa.RSAPublicKey) -> None:
    """Validate that the private and public keys are a matching pair"""
    public_numbers = public_key.public_numbers()
    if public_numbers.e != 65537:
        raise InvalidRsaKeyError(f"unexpected public exponent. Expected 65537, got {public_numbers.e}", KeyType.PUBLIC)
    if private_key.public_key().public_numbers().n != public_numbers.n:
        raise KeyMismatchError(
            f"the keys do not form a pair (the moduli differ). Derive the public key with: {_PUBLIC_FROM_PRIVATE_FIX}")
