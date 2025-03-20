from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class ExportStatement:
  statement_format: str
  date_start: str
  date_end: str
  regional_format: Optional[str]
  include_attachment: Optional[bool]
