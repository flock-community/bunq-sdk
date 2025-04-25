from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class CardBatchReplace:
  cards: 'List[CardBatchReplaceEntry]'

from ..model.CardBatchReplaceEntry import CardBatchReplaceEntry