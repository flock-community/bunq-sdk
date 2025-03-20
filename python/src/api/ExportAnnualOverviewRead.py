from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .LabelUser import LabelUser

@dataclass
class ExportAnnualOverviewRead:
  id: Optional[int]
  created: Optional[str]
  updated: Optional[str]
  year: Optional[int]
  alias_user: Optional[LabelUser]
