from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class MonetaryAccountProfileDrain:
  status: 'Optional[str]'
  balance_preferred: 'Optional[Amount]'
  balance_threshold_high: 'Optional[Amount]'
  savings_account_alias: 'Optional[LabelMonetaryAccount]'

from .Amount import Amount
from .LabelMonetaryAccount import LabelMonetaryAccount