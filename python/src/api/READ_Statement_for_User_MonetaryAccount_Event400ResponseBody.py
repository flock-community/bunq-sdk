from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .ErrorArray import ErrorArray

@dataclass
class READ_Statement_for_User_MonetaryAccount_Event400ResponseBody:
  Error: Optional[List[ErrorArray]]
