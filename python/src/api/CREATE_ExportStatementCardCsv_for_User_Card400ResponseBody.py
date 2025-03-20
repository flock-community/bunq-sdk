from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .ErrorArray import ErrorArray

@dataclass
class CREATE_ExportStatementCardCsv_for_User_Card400ResponseBody:
  Error: Optional[List[ErrorArray]]
