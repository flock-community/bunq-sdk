from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .PaymentAutoAllocateDefinition import PaymentAutoAllocateDefinition

@dataclass
class PaymentAutoAllocate:
  payment_id: int
  type: str
  definition: List[PaymentAutoAllocateDefinition]
