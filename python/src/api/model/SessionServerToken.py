from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class SessionServerToken:
  id: 'Optional[int]'
  token: 'Optional[str]'

