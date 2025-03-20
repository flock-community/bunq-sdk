from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class ExportStatementCardCsvListing:
  id: Optional[int]
  created: Optional[str]
  updated: Optional[str]
  date_start: Optional[str]
  date_end: Optional[str]
  status: Optional[str]
  regional_format: Optional[str]
  card_id: Optional[int]
