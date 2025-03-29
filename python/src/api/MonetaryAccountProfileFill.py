from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class MonetaryAccountProfileFill:
  status: 'Optional[str]'
  balance_preferred: 'Optional[Amount]'
  balance_threshold_low: 'Optional[Amount]'
  issuer: 'Optional[Issuer]'

from .Amount import Amount
from .Issuer import Issuer