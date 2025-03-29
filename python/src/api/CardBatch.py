from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class CardBatch:
  cards: 'List[CardBatchEntry]'

from .CardBatchEntry import CardBatchEntry