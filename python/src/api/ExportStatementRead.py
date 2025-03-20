from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .LabelMonetaryAccount import LabelMonetaryAccount

@dataclass
class ExportStatementRead:
  id: Optional[int]
  created: Optional[str]
  updated: Optional[str]
  date_start: Optional[str]
  date_end: Optional[str]
  status: Optional[str]
  statement_number: Optional[int]
  statement_format: Optional[str]
  regional_format: Optional[str]
  alias_monetary_account: Optional[LabelMonetaryAccount]
