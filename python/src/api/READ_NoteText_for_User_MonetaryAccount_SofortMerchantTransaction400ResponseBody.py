from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class READ_NoteText_for_User_MonetaryAccount_SofortMerchantTransaction400ResponseBody:
  Error: 'Optional[List[ErrorArray]]'

from .ErrorArray import ErrorArray