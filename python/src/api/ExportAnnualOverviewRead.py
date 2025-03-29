from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class ExportAnnualOverviewRead:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  year: 'Optional[int]'
  alias_user: 'Optional[LabelUser]'

from .LabelUser import LabelUser