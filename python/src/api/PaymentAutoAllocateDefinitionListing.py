from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class PaymentAutoAllocateDefinitionListing:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  counterparty_alias: 'Optional[Pointer]'
  description: 'Optional[str]'
  amount: 'Optional[Amount]'
  fraction: 'Optional[int]'

from .Pointer import Pointer
from .Amount import Amount