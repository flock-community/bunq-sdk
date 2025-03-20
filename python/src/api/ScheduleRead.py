from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .ScheduleAnchorObject import ScheduleAnchorObject

@dataclass
class ScheduleRead:
  time_start: Optional[str]
  time_end: Optional[str]
  recurrence_unit: Optional[str]
  recurrence_size: Optional[int]
  status: Optional[str]
  object: Optional[ScheduleAnchorObject]
