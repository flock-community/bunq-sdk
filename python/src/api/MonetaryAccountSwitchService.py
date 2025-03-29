from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class MonetaryAccountSwitchService:
  id: 'Optional[int]'
  created: 'Optional[str]'
  description: 'Optional[str]'
  status: 'Optional[str]'
  sub_status: 'Optional[str]'

