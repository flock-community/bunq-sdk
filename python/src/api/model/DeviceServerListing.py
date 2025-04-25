from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class DeviceServerListing:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  description: 'Optional[str]'
  ip: 'Optional[str]'
  status: 'Optional[str]'

