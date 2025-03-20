from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class UserLegalNameListing:
  legal_names: Optional[List[str]]
