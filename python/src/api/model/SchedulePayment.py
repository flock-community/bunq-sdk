from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class SchedulePayment:
  payment: 'Optional[SchedulePaymentEntry]'
  schedule: 'Optional[Schedule]'
  status: 'Optional[str]'

from ..model.SchedulePaymentEntry import SchedulePaymentEntry
from ..model.Schedule import Schedule