from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class ExportStatementCardCsv:
  date_start: 'str'
  date_end: 'str'
  regional_format: 'str'

