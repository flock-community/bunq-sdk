from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class CardBatchReplaceEntry:
  id: 'int'
  name_on_card: 'Optional[str]'
  pin_code_assignment: 'Optional[List[CardPinAssignment]]'
  second_line: 'Optional[str]'

from .CardPinAssignment import CardPinAssignment