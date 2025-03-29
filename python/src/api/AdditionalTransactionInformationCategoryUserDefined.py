from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class AdditionalTransactionInformationCategoryUserDefined:
  category: 'Optional[str]'
  status: 'str'
  description: 'Optional[str]'
  color: 'Optional[str]'
  icon: 'Optional[str]'

