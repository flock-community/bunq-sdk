from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class TransferwiseCurrencyListing:
  currency: 'Optional[str]'
  name: 'Optional[str]'
  country: 'Optional[str]'

