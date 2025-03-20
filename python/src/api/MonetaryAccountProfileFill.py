from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Amount import Amount
from .Issuer import Issuer

@dataclass
class MonetaryAccountProfileFill:
  status: Optional[str]
  balance_preferred: Optional[Amount]
  balance_threshold_low: Optional[Amount]
  issuer: Optional[Issuer]
