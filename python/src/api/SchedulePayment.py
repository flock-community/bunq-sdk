from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .SchedulePaymentEntry import SchedulePaymentEntry
from .Schedule import Schedule

@dataclass
class SchedulePayment:
  payment: Optional[SchedulePaymentEntry]
  schedule: Optional[Schedule]
  status: Optional[str]
