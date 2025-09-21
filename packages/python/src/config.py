from dataclasses import dataclass
from typing import Optional
from bunq_server import BunqServer
from signing_keys import SigningKeys, SigningKeysFromPem


@dataclass
class Config:
    """Configuration class for bunq API client containing all necessary settings and credentials
    for establishing and managing API connections.
    
    All parameters are validated upon construction to ensure proper format and compatibility.
    """
    bunq_server: BunqServer
    service_name: str
    api_key: str
    signing_keys: SigningKeys
    user_agent: Optional[str] = None
    cache_control: Optional[str] = None
    language: Optional[str] = None
    region: Optional[str] = None
    client_request_id: Optional[str] = None
    geolocation: Optional[str] = None
    
    def __post_init__(self):
        """Validate configuration parameters after initialization"""
        self._validate_basic_parameters()
    
    def _validate_basic_parameters(self):
        """Validate basic configuration parameters"""
        if not self.service_name or not self.service_name.strip():
            raise ValueError("Service name cannot be blank")
        if not self.api_key or not self.api_key.strip():
            raise ValueError("API key cannot be blank")


def create_config(
    bunq_server: BunqServer,
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
    The configuration is validated during construction.
    """
    signing_keys = SigningKeysFromPem(private_key_pem, public_key_pem)
    
    return Config(
        bunq_server=bunq_server,
        service_name=service_name,
        api_key=api_key,
        signing_keys=signing_keys,
        user_agent=user_agent,
        cache_control=cache_control,
        language=language,
        region=region,
        client_request_id=client_request_id,
        geolocation=geolocation
    )
