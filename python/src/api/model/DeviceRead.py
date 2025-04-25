from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class DeviceRead:
  DeviceServer: 'Optional[DeviceServer]'

from ..model.DeviceServer import DeviceServer