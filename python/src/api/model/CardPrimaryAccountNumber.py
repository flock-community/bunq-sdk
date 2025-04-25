from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class CardPrimaryAccountNumber:
  id: 'Optional[int]'
  description: 'Optional[str]'
  status: 'Optional[str]'
  monetary_account_id: 'Optional[int]'
  uuid: 'Optional[str]'
  four_digit: 'Optional[str]'
  type: 'Optional[str]'

