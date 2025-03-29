from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class BunqMeTabResultResponse:
  payment: 'Optional[Payment]'

from .Payment import Payment