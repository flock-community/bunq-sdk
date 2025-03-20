from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .PermittedDevice import PermittedDevice

@dataclass
class PaymentServiceProviderCredentialRead:
  id: Optional[int]
  created: Optional[str]
  updated: Optional[str]
  status: Optional[str]
  expiry_time: Optional[str]
  token_value: Optional[str]
  permitted_device: Optional[PermittedDevice]
