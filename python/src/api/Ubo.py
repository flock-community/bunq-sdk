from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class Ubo:
  name: 'Optional[str]'
  date_of_birth: 'Optional[str]'
  nationality: 'Optional[str]'

