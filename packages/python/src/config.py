from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    service_name: str
    api_key: str
    private_key_file: str = "../private_key.pem"
    public_key_file: str = "../public_key.pem"
    user_agent: Optional[str] = None
    cache_control: Optional[str] = None
    language: Optional[str] = None
    region: Optional[str] = None
    client_request_id: Optional[str] = None
    geolocation: Optional[str] = None
