from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class CurrencyConversionQuote:
  amount: 'Amount'
  currency_source: 'str'
  currency_target: 'str'
  order_type: 'str'
  counterparty_alias: 'Pointer'
  status: 'Optional[str]'

from ..model.Amount import Amount
from ..model.Pointer import Pointer