from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class PaymentAutoAllocateInstance:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  payment_auto_allocate_id: 'Optional[int]'
  status: 'Optional[str]'
  error_message: 'Optional[List[List[ErrorArray]]]'
  payment_batch: 'Optional[PaymentBatch]'
  payment_id: 'Optional[int]'
  all_ginmon_transaction_order: 'Optional[List[GinmonTransaction]]'

from ..model.ErrorArray import ErrorArray
from ..model.PaymentBatch import PaymentBatch
from ..model.GinmonTransaction import GinmonTransaction