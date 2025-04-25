from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class CardCountryPermission:
  country: 'Optional[str]'
  expiry_time: 'Optional[str]'
  id: 'Optional[int]'

