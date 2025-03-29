from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class TransferwiseQuoteTemporary:
  currency_source: 'str'
  currency_target: 'str'
  amount_source: 'Optional[Amount]'
  amount_target: 'Optional[Amount]'

from .Amount import Amount