from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class ExportStatementCardPdfListing:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  date_start: 'Optional[str]'
  date_end: 'Optional[str]'
  status: 'Optional[str]'
  card_id: 'Optional[int]'

