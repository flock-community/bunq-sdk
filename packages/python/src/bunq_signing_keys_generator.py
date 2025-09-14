"""
Bunq signing keys generator utility for handling cryptographic key generation.
Provides methods to generate SigningKeys implementations for bunq API usage.
"""

import os
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from typing import Tuple, Union

from signing_keys import SigningKeys, SigningKeysFromRsa, SigningKeysFromPem


class BunqSigningKeysGenerator:
    """Bunq signing keys generator for creating SigningKeys implementations"""
    
    @staticmethod
    def generate_bunq_signing_keys() -> SigningKeys:
        """
        Generates an RSA key pair using 2048-bit key size.
        
        Returns:
            SigningKeys: A SigningKeys implementation containing the generated key pair
        """
        print('bunq - created new keypair [KEEP IT SAFE]')
        
        # Generate new RSA keys with 2048 bits as required by bunq
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        
        return SigningKeysFromRsa(private_key, public_key)
    
    @staticmethod
    def generate_bunq_signing_keys_with_files(private_key_file: Union[str, Path], public_key_file: Union[str, Path]) -> SigningKeys:
        """
        Generates and stores an RSA key pair in the specified files. If the files already exist,
        the existing key pair will be reused. The key pair is generated using a 2048-bit key size.
        
        Args:
            private_key_file: The file where the generated private key will be stored or retrieved from if it already exists
            public_key_file: The file where the generated public key will be stored or retrieved from if it already exists
            
        Returns:
            SigningKeys: A SigningKeys implementation containing the key pair
        """
        private_key_path = Path(private_key_file)
        public_key_path = Path(public_key_file)
        
        if private_key_path.exists() and public_key_path.exists():
            print('bunq - using existing keypair')
            private_key_pem = private_key_path.read_text(encoding='utf-8')
            public_key_pem = public_key_path.read_text(encoding='utf-8')
            return SigningKeysFromPem(private_key_pem, public_key_pem)
        
        # Generate new signing keys
        signing_keys = BunqSigningKeysGenerator.generate_bunq_signing_keys()
        
        # Ensure parent directories exist
        private_key_path.parent.mkdir(parents=True, exist_ok=True)
        public_key_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write keys to files
        private_key_path.write_text(signing_keys.private_key_as_pem(), encoding='utf-8')
        public_key_path.write_text(signing_keys.public_key_as_pem(), encoding='utf-8')
        
        print('bunq - created new keypair [KEEP THESE FILES SAFE]')
        return signing_keys
    
    @staticmethod
    def generate_bunq_signing_keys_as_pem() -> Tuple[str, str]:
        """
        Generates an RSA key pair and returns the keys as PEM strings.
        
        Returns:
            Tuple[str, str]: A tuple containing the private key as the first element and the public key 
            as the second element, both represented as strings in PEM format.
        """
        signing_keys = BunqSigningKeysGenerator.generate_bunq_signing_keys()
        return signing_keys.private_key_as_pem(), signing_keys.public_key_as_pem()