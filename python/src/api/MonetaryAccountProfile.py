from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .MonetaryAccountProfileFill import MonetaryAccountProfileFill
from .MonetaryAccountProfileDrain import MonetaryAccountProfileDrain

@dataclass
class MonetaryAccountProfile:
  profile_fill: Optional[MonetaryAccountProfileFill]
  profile_drain: Optional[MonetaryAccountProfileDrain]
