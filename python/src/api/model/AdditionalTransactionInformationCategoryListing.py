from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class AdditionalTransactionInformationCategoryListing:
  category: 'Optional[str]'
  type: 'Optional[str]'
  status: 'Optional[str]'
  order: 'Optional[int]'
  description: 'Optional[str]'
  description_translated: 'Optional[str]'
  color: 'Optional[str]'
  icon: 'Optional[str]'

