from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class READ_ScheduleInstance_for_User_MonetaryAccount_Schedule400ResponseBody:
  Error: 'Optional[List[ErrorArray]]'

from ..model.ErrorArray import ErrorArray