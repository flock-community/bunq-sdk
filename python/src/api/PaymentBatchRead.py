from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .PaymentBatchAnchoredPayment import PaymentBatchAnchoredPayment

@dataclass
class PaymentBatchRead:
  payments: Optional[PaymentBatchAnchoredPayment]
