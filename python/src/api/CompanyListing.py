from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .UserCompany import UserCompany

@dataclass
class CompanyListing:
  UserCompany: Optional[UserCompany]
