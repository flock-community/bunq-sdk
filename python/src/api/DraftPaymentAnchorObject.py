from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Payment import Payment
from .PaymentBatch import PaymentBatch

@dataclass
class DraftPaymentAnchorObject:
  Payment: Optional[Payment]
  PaymentBatch: Optional[PaymentBatch]
