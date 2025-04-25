from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class PaymentAutoAllocateRead:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  type: 'Optional[str]'
  status: 'Optional[str]'
  trigger_amount: 'Optional[Amount]'
  payment: 'Optional[Payment]'
  payment_original: 'Optional[Payment]'
  payment_latest: 'Optional[Payment]'

from ..model.Amount import Amount
from ..model.Payment import Payment