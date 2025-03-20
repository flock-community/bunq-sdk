from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class TransferwiseUserListing:
  id: Optional[int]
  created: Optional[str]
  updated: Optional[str]
  name: Optional[str]
  email: Optional[str]
  source: Optional[str]
