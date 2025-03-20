from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .CardBatchReplaceEntry import CardBatchReplaceEntry

@dataclass
class CardBatchReplace:
  cards: List[CardBatchReplaceEntry]
