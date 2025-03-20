from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .ErrorArray import ErrorArray

@dataclass
class CREATE_MonetaryAccountExternal_for_User400ResponseBody:
  Error: Optional[List[ErrorArray]]
