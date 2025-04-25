from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class DraftPaymentAnchorObject:
  Payment: 'Optional[Payment]'
  PaymentBatch: 'Optional[PaymentBatch]'

from ..model.Payment import Payment
from ..model.PaymentBatch import PaymentBatch