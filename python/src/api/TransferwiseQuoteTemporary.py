from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Amount import Amount

@dataclass
class TransferwiseQuoteTemporary:
  currency_source: str
  currency_target: str
  amount_source: Optional[Amount]
  amount_target: Optional[Amount]
