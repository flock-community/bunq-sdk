from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class PermittedDevice:
  description: Optional[str]
  ip: Optional[str]
