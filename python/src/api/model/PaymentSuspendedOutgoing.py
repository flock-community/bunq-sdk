from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class PaymentSuspendedOutgoing:
  status: 'Optional[str]'
  monetary_account_id: 'Optional[str]'
  time_execution: 'Optional[str]'

