from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Amount import Amount
from .Payment import Payment

@dataclass
class PaymentAutoAllocateRead:
  id: Optional[int]
  created: Optional[str]
  updated: Optional[str]
  type: Optional[str]
  status: Optional[str]
  trigger_amount: Optional[Amount]
  payment: Optional[Payment]
  payment_original: Optional[Payment]
  payment_latest: Optional[Payment]
