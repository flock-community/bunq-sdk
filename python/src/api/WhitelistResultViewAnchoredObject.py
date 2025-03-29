from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class WhitelistResultViewAnchoredObject:
  id: 'Optional[int]'
  requestResponse: 'Optional[RequestResponse]'
  draftPayment: 'Optional[DraftPayment]'

from .RequestResponse import RequestResponse
from .DraftPayment import DraftPayment