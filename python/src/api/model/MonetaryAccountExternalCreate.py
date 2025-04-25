from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class MonetaryAccountExternalCreate:
  Id: 'Optional[BunqId]'

from ..model.BunqId import BunqId