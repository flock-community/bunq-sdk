from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class List_all_Payment_for_User_MonetaryAccount400ResponseBody:
  Error: 'Optional[List[ErrorArray]]'

from .ErrorArray import ErrorArray