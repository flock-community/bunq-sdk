from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class ScheduleInstanceRead:
  state: 'Optional[str]'
  time_start: 'Optional[str]'
  time_end: 'Optional[str]'
  error_message: 'Optional[List[List[ErrorArray]]]'
  scheduled_object: 'Optional[ScheduleAnchorObject]'
  result_object: 'Optional[ScheduleInstanceAnchorObject]'
  request_reference_split_the_bill: 'Optional[List[RequestInquiryReference]]'

from ..model.ErrorArray import ErrorArray
from ..model.ScheduleAnchorObject import ScheduleAnchorObject
from ..model.ScheduleInstanceAnchorObject import ScheduleInstanceAnchorObject
from ..model.RequestInquiryReference import RequestInquiryReference