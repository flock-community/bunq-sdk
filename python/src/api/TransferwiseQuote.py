from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Amount import Amount

@dataclass
class TransferwiseQuote:
  currency_source: str
  currency_target: str
  amount_source: Optional[Amount]
  amount_target: Optional[Amount]
  id: Optional[int]
  created: Optional[str]
  updated: Optional[str]
  time_expiry: Optional[str]
  quote_id: Optional[str]
  amount_fee: Optional[Amount]
  rate: Optional[str]
  time_delivery_estimate: Optional[str]
