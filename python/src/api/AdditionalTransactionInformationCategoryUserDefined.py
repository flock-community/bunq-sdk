from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class AdditionalTransactionInformationCategoryUserDefined:
  category: Optional[str]
  status: str
  description: Optional[str]
  color: Optional[str]
  icon: Optional[str]
