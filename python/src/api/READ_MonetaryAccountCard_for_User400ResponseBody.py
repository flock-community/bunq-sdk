from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .ErrorArray import ErrorArray

@dataclass
class READ_MonetaryAccountCard_for_User400ResponseBody:
  Error: Optional[List[ErrorArray]]
