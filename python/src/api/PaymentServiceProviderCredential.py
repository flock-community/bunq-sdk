from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class PaymentServiceProviderCredential:
  client_payment_service_provider_certificate: str
  client_payment_service_provider_certificate_chain: str
  client_public_key_signature: str
