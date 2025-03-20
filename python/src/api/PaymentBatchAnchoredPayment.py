from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Payment import Payment

@dataclass
class PaymentBatchAnchoredPayment:
  Payment: Optional[List[Payment]]
