from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class CardNameListing:
  possible_card_name_array: Optional[List[str]]
