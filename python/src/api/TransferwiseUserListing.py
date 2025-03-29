from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class TransferwiseUserListing:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  name: 'Optional[str]'
  email: 'Optional[str]'
  source: 'Optional[str]'

