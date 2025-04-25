from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class ExportStatementCardPdf:
  date_start: 'str'
  date_end: 'str'

