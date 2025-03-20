from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Pointer import Pointer
from .Amount import Amount

@dataclass
class PaymentAutoAllocateDefinition:
  type: str
  counterparty_alias: Optional[Pointer]
  description: Optional[str]
  amount: Optional[Amount]
  fraction: Optional[int]
  id: Optional[int]
  created: Optional[str]
  updated: Optional[str]
