from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Amount import Amount
from .Pointer import Pointer

@dataclass
class CurrencyConversionQuote:
  amount: Amount
  currency_source: str
  currency_target: str
  order_type: str
  counterparty_alias: Pointer
  status: Optional[str]
