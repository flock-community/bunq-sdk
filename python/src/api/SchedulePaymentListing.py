from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class SchedulePaymentListing:
  payment: 'Optional[SchedulePaymentEntry]'
  schedule: 'Optional[Schedule]'
  status: 'Optional[str]'

from .SchedulePaymentEntry import SchedulePaymentEntry
from .Schedule import Schedule