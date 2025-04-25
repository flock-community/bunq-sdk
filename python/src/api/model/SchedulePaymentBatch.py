from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class SchedulePaymentBatch:
  payments: 'Optional[List[SchedulePaymentEntry]]'
  schedule: 'Optional[Schedule]'

from ..model.SchedulePaymentEntry import SchedulePaymentEntry
from ..model.Schedule import Schedule