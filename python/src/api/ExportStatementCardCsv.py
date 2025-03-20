from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class ExportStatementCardCsv:
  date_start: str
  date_end: str
  regional_format: str
