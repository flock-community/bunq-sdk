from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class PaymentServiceProviderCredentialRead:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  status: 'Optional[str]'
  expiry_time: 'Optional[str]'
  token_value: 'Optional[str]'
  permitted_device: 'Optional[PermittedDevice]'

from .PermittedDevice import PermittedDevice