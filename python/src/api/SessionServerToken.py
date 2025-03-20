from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class SessionServerToken:
  id: Optional[int]
  token: Optional[str]
