from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .ErrorArray import ErrorArray

@dataclass
class List_all_Name_for_UserCompany400ResponseBody:
  Error: Optional[List[ErrorArray]]
