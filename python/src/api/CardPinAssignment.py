from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class CardPinAssignment:
  type: 'Optional[str]'
  routing_type: 'Optional[str]'
  pin_code: 'Optional[str]'
  monetary_account_id: 'Optional[int]'
  status: 'Optional[str]'

