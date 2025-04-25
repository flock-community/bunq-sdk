from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class CardReplace:
  name_on_card: 'Optional[str]'
  preferred_name_on_card: 'Optional[str]'
  pin_code_assignment: 'Optional[List[CardPinAssignment]]'
  second_line: 'Optional[str]'

from ..model.CardPinAssignment import CardPinAssignment