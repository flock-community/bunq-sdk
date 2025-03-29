from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class CurrencyConversionQuote:
  amount: 'Amount'
  currency_source: 'str'
  currency_target: 'str'
  order_type: 'str'
  counterparty_alias: 'Pointer'
  status: 'Optional[str]'

from .Amount import Amount
from .Pointer import Pointer