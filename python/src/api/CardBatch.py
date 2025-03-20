from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .CardBatchEntry import CardBatchEntry

@dataclass
class CardBatch:
  cards: List[CardBatchEntry]
