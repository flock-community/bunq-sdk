from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class Pointer:
  type: 'Optional[str]'
  value: 'Optional[str]'
  name: 'Optional[str]'
  service: 'Optional[str]'

