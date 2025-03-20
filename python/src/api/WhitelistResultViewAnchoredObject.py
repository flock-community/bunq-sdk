from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .RequestResponse import RequestResponse
from .DraftPayment import DraftPayment

@dataclass
class WhitelistResultViewAnchoredObject:
  id: Optional[int]
  requestResponse: Optional[RequestResponse]
  draftPayment: Optional[DraftPayment]
