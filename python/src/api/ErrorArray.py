from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class ErrorArray:
  error_description: 'Optional[str]'
  error_description_translated: 'Optional[str]'

