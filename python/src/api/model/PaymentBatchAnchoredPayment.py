from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class PaymentBatchAnchoredPayment:
  Payment: 'Optional[List[Payment]]'

from ..model.Payment import Payment