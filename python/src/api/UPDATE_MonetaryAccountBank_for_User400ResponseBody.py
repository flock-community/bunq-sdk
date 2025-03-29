from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class UPDATE_MonetaryAccountBank_for_User400ResponseBody:
  Error: 'Optional[List[ErrorArray]]'

from .ErrorArray import ErrorArray