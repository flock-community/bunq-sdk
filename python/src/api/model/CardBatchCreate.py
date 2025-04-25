from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class CardBatchCreate:
  updated_card_ids: 'Optional[List[BunqId]]'

from ..model.BunqId import BunqId