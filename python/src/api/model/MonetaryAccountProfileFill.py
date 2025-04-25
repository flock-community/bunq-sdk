from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class MonetaryAccountProfileFill:
  status: 'Optional[str]'
  balance_preferred: 'Optional[Amount]'
  balance_threshold_low: 'Optional[Amount]'
  issuer: 'Optional[Issuer]'

from ..model.Amount import Amount
from ..model.Issuer import Issuer