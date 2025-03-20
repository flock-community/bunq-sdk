from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class ErrorArray:
  error_description: Optional[str]
  error_description_translated: Optional[str]
