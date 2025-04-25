from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class TransferwiseQuoteTemporaryRead:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  time_expiry: 'Optional[str]'
  quote_id: 'Optional[str]'
  amount_source: 'Optional[Amount]'
  amount_target: 'Optional[Amount]'
  rate: 'Optional[str]'

from ..model.Amount import Amount