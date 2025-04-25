from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class DeviceServerCreate:
  Id: 'Optional[DeviceServerCreateId]'

from ..model.DeviceServerCreateId import DeviceServerCreateId