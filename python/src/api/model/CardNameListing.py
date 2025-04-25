from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class CardNameListing:
  possible_card_name_array: 'Optional[List[str]]'

