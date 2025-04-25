from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class InsightListing:
  category: 'Optional[str]'
  category_translated: 'Optional[str]'
  category_color: 'Optional[str]'
  category_icon: 'Optional[str]'
  amount_total: 'Optional[Amount]'
  number_of_transactions: 'Optional[int]'

from ..model.Amount import Amount