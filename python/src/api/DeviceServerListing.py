from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class DeviceServerListing:
  id: Optional[int]
  created: Optional[str]
  updated: Optional[str]
  description: Optional[str]
  ip: Optional[str]
  status: Optional[str]
