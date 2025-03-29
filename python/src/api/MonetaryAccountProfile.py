from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class MonetaryAccountProfile:
  profile_fill: 'Optional[MonetaryAccountProfileFill]'
  profile_drain: 'Optional[MonetaryAccountProfileDrain]'

from .MonetaryAccountProfileFill import MonetaryAccountProfileFill
from .MonetaryAccountProfileDrain import MonetaryAccountProfileDrain