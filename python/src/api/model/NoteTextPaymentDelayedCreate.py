from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class NoteTextPaymentDelayedCreate:
  Id: 'Optional[BunqId]'

from ..model.BunqId import BunqId