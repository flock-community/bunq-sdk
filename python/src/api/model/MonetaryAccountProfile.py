from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class MonetaryAccountProfile:
  profile_fill: 'Optional[MonetaryAccountProfileFill]'
  profile_drain: 'Optional[MonetaryAccountProfileDrain]'

from ..model.MonetaryAccountProfileFill import MonetaryAccountProfileFill
from ..model.MonetaryAccountProfileDrain import MonetaryAccountProfileDrain