from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .ErrorArray import ErrorArray
from .PaymentBatch import PaymentBatch
from .GinmonTransaction import GinmonTransaction

@dataclass
class PaymentAutoAllocateInstanceListing:
  id: Optional[int]
  created: Optional[str]
  updated: Optional[str]
  payment_auto_allocate_id: Optional[int]
  status: Optional[str]
  error_message: Optional[List[List[ErrorArray]]]
  payment_batch: Optional[PaymentBatch]
  payment_id: Optional[int]
  all_ginmon_transaction_order: Optional[List[GinmonTransaction]]
