from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class MonetaryAccountSwitchService:
  id: Optional[int]
  created: Optional[str]
  description: Optional[str]
  status: Optional[str]
  sub_status: Optional[str]
