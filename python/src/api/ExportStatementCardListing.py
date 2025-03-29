from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class ExportStatementCardListing:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  date_start: 'Optional[str]'
  date_end: 'Optional[str]'
  status: 'Optional[str]'
  regional_format: 'Optional[str]'
  card_id: 'Optional[int]'

