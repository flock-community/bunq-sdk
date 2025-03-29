from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class CompanyRead:
  UserCompany: 'Optional[UserCompany]'

from .UserCompany import UserCompany