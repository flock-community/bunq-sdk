from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class SchedulePaymentBatch:
  payments: 'Optional[List[SchedulePaymentEntry]]'
  schedule: 'Optional[Schedule]'

from .SchedulePaymentEntry import SchedulePaymentEntry
from .Schedule import Schedule