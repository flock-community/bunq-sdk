from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .PaymentAutoAllocate import PaymentAutoAllocate

@dataclass
class PaymentAutoAllocateUserListing:
  PaymentAutoAllocate: Optional[PaymentAutoAllocate]
