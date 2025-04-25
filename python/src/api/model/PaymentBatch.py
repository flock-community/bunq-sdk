from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class PaymentBatch:
  payments: 'Optional[PaymentBatchAnchoredPayment]'

from ..model.PaymentBatchAnchoredPayment import PaymentBatchAnchoredPayment