from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .DeviceServer import DeviceServer

@dataclass
class DeviceListing:
  DeviceServer: Optional[DeviceServer]
