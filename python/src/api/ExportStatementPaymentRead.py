from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class ExportStatementPaymentRead:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  status: 'Optional[str]'

