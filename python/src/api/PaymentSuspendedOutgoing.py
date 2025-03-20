from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class PaymentSuspendedOutgoing:
  status: Optional[str]
  monetary_account_id: Optional[str]
  time_execution: Optional[str]
