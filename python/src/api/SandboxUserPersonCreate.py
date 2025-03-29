from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class SandboxUserPersonCreate:
  Id: 'Optional[BunqId]'

from .BunqId import BunqId