from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class CardBatchReplace:
  cards: 'List[CardBatchReplaceEntry]'

from .CardBatchReplaceEntry import CardBatchReplaceEntry