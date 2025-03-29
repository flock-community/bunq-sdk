from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class SchedulePaymentBatchCreate:
  Id: 'Optional[BunqId]'

from .BunqId import BunqId