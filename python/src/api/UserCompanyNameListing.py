from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class UserCompanyNameListing:
  name_array: Optional[List[str]]
