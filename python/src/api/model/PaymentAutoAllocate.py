from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class PaymentAutoAllocate:
  payment_id: 'int'
  type: 'str'
  definition: 'List[PaymentAutoAllocateDefinition]'

from ..model.PaymentAutoAllocateDefinition import PaymentAutoAllocateDefinition