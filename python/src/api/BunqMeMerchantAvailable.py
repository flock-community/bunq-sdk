from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class BunqMeMerchantAvailable:
  merchant_type: Optional[str]
  available: Optional[bool]
