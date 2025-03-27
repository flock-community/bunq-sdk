from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .DeviceServerCreateId import DeviceServerCreateId

@dataclass
class DeviceServerCreate:
  Id: Optional[DeviceServerCreateId]
