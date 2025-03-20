from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Pointer import Pointer
from .CardPinAssignment import CardPinAssignment

@dataclass
class CardDebit:
  second_line: str
  name_on_card: str
  preferred_name_on_card: Optional[str]
  alias: Optional[Pointer]
  type: str
  product_type: str
  pin_code_assignment: Optional[List[CardPinAssignment]]
  monetary_account_id_fallback: Optional[int]
  order_status: Optional[str]
