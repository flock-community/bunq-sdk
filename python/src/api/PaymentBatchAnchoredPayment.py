from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class PaymentBatchAnchoredPayment:
  Payment: 'Optional[List[Payment]]'

from .Payment import Payment