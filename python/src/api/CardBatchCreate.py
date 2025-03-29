from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class CardBatchCreate:
  updated_card_ids: 'Optional[List[BunqId]]'

from .BunqId import BunqId