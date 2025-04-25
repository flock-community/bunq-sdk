from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class BunqMeTabResultResponseRead:
  payment: 'Optional[Payment]'

from ..model.Payment import Payment