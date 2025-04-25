from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class CREATE_NoteText_for_User_MonetaryAccount_PaymentDelayed400ResponseBody:
  Error: 'Optional[List[ErrorArray]]'

from ..model.ErrorArray import ErrorArray