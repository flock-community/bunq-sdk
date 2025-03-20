from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class CardPrimaryAccountNumber:
  id: Optional[int]
  description: Optional[str]
  status: Optional[str]
  monetary_account_id: Optional[int]
  uuid: Optional[str]
  four_digit: Optional[str]
  type: Optional[str]
