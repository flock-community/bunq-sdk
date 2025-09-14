"""
SigningKeys sealed hierarchy for RSA key pairs used in bunq API request signing.

Provides consistent access to both PEM string representations and parsed 
RSA key objects, ensuring they remain synchronized.
"""

from abc import ABC, abstractmethod
from typing import Final
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature


class ConfigValidationError(Exception):
    """Base exception for configuration validation errors"""
    def __init__(self, message: str, cause: Exception = None):
        super().__init__(message)
        self.cause = cause


class InvalidPemFormatError(ConfigValidationError):
    """Error thrown when PEM format validation fails"""
    pass


class InvalidRsaKeyError(ConfigValidationError):
    """Error thrown when RSA key validation fails"""
    pass


class KeyMismatchError(ConfigValidationError):
    """Error thrown when private and public keys don't match"""
    pass


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


def _validate_and_load_private_key(private_key_pem: str) -> rsa.RSAPrivateKey:
    """Validate and load a private key from PEM format"""
    try:
        if "-----BEGIN PRIVATE KEY-----" not in private_key_pem or \
           "-----END PRIVATE KEY-----" not in private_key_pem:
            raise InvalidPemFormatError("Private key must be in PKCS#8 PEM format")
        
        private_key = serialization.load_pem_private_key(
            private_key_pem.encode('utf-8'),
            password=None
        )
        
        if not isinstance(private_key, rsa.RSAPrivateKey):
            raise InvalidRsaKeyError("Private key must be an RSA key")
        
        return private_key
    except ConfigValidationError:
        raise
    except Exception as e:
        raise InvalidRsaKeyError(f"Failed to load private key: {str(e)}", e)


def _validate_and_load_public_key(public_key_pem: str) -> rsa.RSAPublicKey:
    """Validate and load a public key from PEM format"""
    try:
        if "-----BEGIN PUBLIC KEY-----" not in public_key_pem or \
           "-----END PUBLIC KEY-----" not in public_key_pem:
            raise InvalidPemFormatError("Public key must be in X.509 PEM format")
        
        public_key = serialization.load_pem_public_key(
            public_key_pem.encode('utf-8')
        )
        
        if not isinstance(public_key, rsa.RSAPublicKey):
            raise InvalidRsaKeyError("Public key must be an RSA key")
        
        return public_key
    except ConfigValidationError:
        raise
    except Exception as e:
        raise InvalidRsaKeyError(f"Failed to load public key: {str(e)}", e)


def _validate_key_compatibility(private_key: rsa.RSAPrivateKey, public_key: rsa.RSAPublicKey):
    """Validate that the private and public keys are a matching pair"""
    try:
        # Verify that the private and public keys are a matching pair
        # by checking that they have the same modulus
        private_public_key = private_key.public_key()
        private_modulus = private_public_key.public_numbers().n
        public_modulus = public_key.public_numbers().n
        
        if private_modulus != public_modulus:
            raise KeyMismatchError("Private and public keys do not form a valid key pair (modulus mismatch)")
        
        # Additional check: verify that the public exponent matches the expected value for RSA
        public_exponent = public_key.public_numbers().e
        if public_exponent != 65537:
            raise InvalidRsaKeyError(f"Public key has unexpected exponent. Expected 65537, got {public_exponent}")
        
        # Final verification: test signing and verification
        test_data = b"test-signature-data"
        signature = private_key.sign(
            test_data,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        
        try:
            public_key.verify(
                signature,
                test_data,
                padding.PKCS1v15(),
                hashes.SHA256()
            )
        except InvalidSignature:
            raise KeyMismatchError("Private and public keys do not form a valid key pair (signature verification failed)")
            
    except ConfigValidationError:
        raise
    except Exception as e:
        raise KeyMismatchError(f"Failed to validate key compatibility: {str(e)}")