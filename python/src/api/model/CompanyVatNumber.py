from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class CompanyVatNumber:
  type: 'Optional[str]'
  country: 'Optional[str]'
  value: 'Optional[str]'

