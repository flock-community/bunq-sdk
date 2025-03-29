from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class ExportRibListing:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'

