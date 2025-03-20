from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .BunqId import BunqId

@dataclass
class TransferwiseQuoteCreate:
  Id: Optional[BunqId]
