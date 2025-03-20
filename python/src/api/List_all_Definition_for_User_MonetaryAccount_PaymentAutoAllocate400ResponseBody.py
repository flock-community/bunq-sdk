from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .ErrorArray import ErrorArray

@dataclass
class List_all_Definition_for_User_MonetaryAccount_PaymentAutoAllocate400ResponseBody:
  Error: Optional[List[ErrorArray]]
