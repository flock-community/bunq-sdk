from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class CardCountryPermission:
  country: Optional[str]
  expiry_time: Optional[str]
  id: Optional[int]
