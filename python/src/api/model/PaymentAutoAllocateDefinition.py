from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class PaymentAutoAllocateDefinition:
  type: 'str'
  counterparty_alias: 'Optional[Pointer]'
  description: 'Optional[str]'
  amount: 'Optional[Amount]'
  fraction: 'Optional[int]'
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'

from ..model.Pointer import Pointer
from ..model.Amount import Amount