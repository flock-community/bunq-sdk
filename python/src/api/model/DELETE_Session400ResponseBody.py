from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class DELETE_Session400ResponseBody:
  Error: 'Optional[List[ErrorArray]]'

from ..model.ErrorArray import ErrorArray