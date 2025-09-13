from dataclasses import dataclass
from typing import Optional
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature
import io


class ConfigValidationError(Exception):
    """Base exception for configuration validation errors"""
    def __init__(self, message: str, cause: Optional[Exception] = None):
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


@dataclass
class Config:
    """Configuration class for bunq API client containing all necessary settings and credentials
    for establishing and managing API connections.
    
    All parameters are validated upon construction to ensure proper format and compatibility.
    """
    service_name: str
    api_key: str
    private_key_pem: str
    public_key_pem: str
    user_agent: Optional[str] = None
    cache_control: Optional[str] = None
    language: Optional[str] = None
    region: Optional[str] = None
    client_request_id: Optional[str] = None
    geolocation: Optional[str] = None
    
    def __post_init__(self):
        """Validate configuration parameters after initialization"""
        self._validate_basic_parameters()
        private_key = self._validate_and_load_private_key()
        public_key = self._validate_and_load_public_key()
        self._validate_key_compatibility(private_key, public_key)
        
        # Store validated keys for later use
        self._private_key = private_key
        self._public_key = public_key
    
    def get_public_key_as_string(self) -> str:
        """Gets the public key as a PEM string for API usage"""
        return self.public_key_pem
    
    def _validate_basic_parameters(self):
        """Validate basic configuration parameters"""
        if not self.service_name or not self.service_name.strip():
            raise ValueError("Service name cannot be blank")
        if not self.api_key or not self.api_key.strip():
            raise ValueError("API key cannot be blank")
    
    def _validate_and_load_private_key(self) -> rsa.RSAPrivateKey:
        """Validate and load the private key"""
        try:
            if "-----BEGIN PRIVATE KEY-----" not in self.private_key_pem or \
               "-----END PRIVATE KEY-----" not in self.private_key_pem:
                raise InvalidPemFormatError("Private key must be in PKCS#8 PEM format")
            
            private_key = serialization.load_pem_private_key(
                self.private_key_pem.encode('utf-8'),
                password=None
            )
            
            if not isinstance(private_key, rsa.RSAPrivateKey):
                raise InvalidRsaKeyError("Private key must be an RSA key")
            
            return private_key
        except ConfigValidationError:
            raise
        except Exception as e:
            raise InvalidRsaKeyError(f"Failed to load private key: {str(e)}", e)
    
    def _validate_and_load_public_key(self) -> rsa.RSAPublicKey:
        """Validate and load the public key"""
        try:
            if "-----BEGIN PUBLIC KEY-----" not in self.public_key_pem or \
               "-----END PUBLIC KEY-----" not in self.public_key_pem:
                raise InvalidPemFormatError("Public key must be in X.509 PEM format")
            
            public_key = serialization.load_pem_public_key(
                self.public_key_pem.encode('utf-8')
            )
            
            if not isinstance(public_key, rsa.RSAPublicKey):
                raise InvalidRsaKeyError("Public key must be an RSA key")
            
            return public_key
        except ConfigValidationError:
            raise
        except Exception as e:
            raise InvalidRsaKeyError(f"Failed to load public key: {str(e)}", e)
    
    def _validate_key_compatibility(self, private_key: rsa.RSAPrivateKey, public_key: rsa.RSAPublicKey):
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


def create_config(
    service_name: str,
    api_key: str,
    private_key_pem: str,
    public_key_pem: str,
    user_agent: Optional[str] = None,
    cache_control: Optional[str] = None,
    language: Optional[str] = None,
    region: Optional[str] = None,
    client_request_id: Optional[str] = None,
    geolocation: Optional[str] = None
) -> Config:
    """Creates and validates a configuration object.
    Raises ConfigValidationError if validation fails.
    """
    return Config(
        service_name=service_name,
        api_key=api_key,
        private_key_pem=private_key_pem,
        public_key_pem=public_key_pem,
        user_agent=user_agent,
        cache_control=cache_control,
        language=language,
        region=region,
        client_request_id=client_request_id,
        geolocation=geolocation
    )
