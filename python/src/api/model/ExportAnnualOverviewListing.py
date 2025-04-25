from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class ExportAnnualOverviewListing:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  year: 'Optional[int]'
  alias_user: 'Optional[LabelUser]'

from ..model.LabelUser import LabelUser