from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class CompanyVatNumber:
  type: Optional[str]
  country: Optional[str]
  value: Optional[str]
