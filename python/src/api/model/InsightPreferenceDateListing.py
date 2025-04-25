from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class InsightPreferenceDateListing:
  day_of_month: 'Optional[int]'

