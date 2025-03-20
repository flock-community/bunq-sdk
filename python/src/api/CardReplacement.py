from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Address import Address

@dataclass
class CardReplacement:
  status: Optional[str]
  address_main: Optional[Address]
  address_postal: Optional[Address]
  card_id: Optional[int]
  card_new_id: Optional[int]
