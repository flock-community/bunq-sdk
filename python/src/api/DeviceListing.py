from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class DeviceListing:
  DeviceServer: 'Optional[DeviceServer]'

from .DeviceServer import DeviceServer