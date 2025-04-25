from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class TaxResident:
  country: 'Optional[str]'
  tax_number: 'Optional[str]'
  status: 'Optional[str]'
  id: 'Optional[int]'

