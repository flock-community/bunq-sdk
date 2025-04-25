from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class CardGeneratedCvc2Update:
  Id: 'Optional[BunqId]'

from ..model.BunqId import BunqId