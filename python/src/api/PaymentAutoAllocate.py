from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class PaymentAutoAllocate:
  payment_id: 'int'
  type: 'str'
  definition: 'List[PaymentAutoAllocateDefinition]'

from .PaymentAutoAllocateDefinition import PaymentAutoAllocateDefinition