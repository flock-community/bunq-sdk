from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .ErrorArray import ErrorArray
from .ScheduleAnchorObject import ScheduleAnchorObject
from .ScheduleInstanceAnchorObject import ScheduleInstanceAnchorObject
from .RequestInquiryReference import RequestInquiryReference

@dataclass
class ScheduleInstance:
  state: Optional[str]
  time_start: Optional[str]
  time_end: Optional[str]
  error_message: Optional[List[List[ErrorArray]]]
  scheduled_object: Optional[ScheduleAnchorObject]
  result_object: Optional[ScheduleInstanceAnchorObject]
  request_reference_split_the_bill: Optional[List[RequestInquiryReference]]
