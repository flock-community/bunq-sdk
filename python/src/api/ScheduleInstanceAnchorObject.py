from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class ScheduleInstanceAnchorObject:
  Payment: 'Optional[Payment]'
  PaymentBatch: 'Optional[PaymentBatch]'

from .Payment import Payment
from .PaymentBatch import PaymentBatch