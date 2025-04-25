from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class Schedule:
  time_start: 'Optional[str]'
  time_end: 'Optional[str]'
  recurrence_unit: 'Optional[str]'
  recurrence_size: 'Optional[int]'
  status: 'Optional[str]'
  object: 'Optional[ScheduleAnchorObject]'

from ..model.ScheduleAnchorObject import ScheduleAnchorObject