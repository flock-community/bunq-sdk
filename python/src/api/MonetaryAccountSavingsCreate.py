from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class MonetaryAccountSavingsCreate:
  Id: 'Optional[BunqId]'

from .BunqId import BunqId