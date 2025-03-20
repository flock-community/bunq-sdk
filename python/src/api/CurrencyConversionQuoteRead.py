from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Amount import Amount

@dataclass
class CurrencyConversionQuoteRead:
  id: Optional[int]
  created: Optional[str]
  updated: Optional[str]
  status: Optional[str]
  amount_source: Optional[Amount]
  amount_target: Optional[Amount]
  rate: Optional[str]
  time_expiry: Optional[str]
