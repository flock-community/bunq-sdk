from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class CardReplacement:
  status: 'Optional[str]'
  address_main: 'Optional[Address]'
  address_postal: 'Optional[Address]'
  card_id: 'Optional[int]'
  card_new_id: 'Optional[int]'

from ..model.Address import Address