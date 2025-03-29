from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class DeviceServerCreate:
  Id: 'Optional[DeviceServerCreateId]'

from .DeviceServerCreateId import DeviceServerCreateId