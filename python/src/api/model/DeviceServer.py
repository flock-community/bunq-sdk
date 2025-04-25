from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class DeviceServer:
  description: 'str'
  secret: 'str'
  permitted_ips: 'Optional[List[str]]'

