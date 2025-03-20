from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class CardGeneratedCvc2Listing:
  id: Optional[int]
  created: Optional[str]
  updated: Optional[str]
  type: Optional[str]
  cvc2: Optional[str]
  status: Optional[str]
  expiry_time: Optional[str]
