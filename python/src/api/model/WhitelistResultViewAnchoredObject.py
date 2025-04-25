from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class WhitelistResultViewAnchoredObject:
  id: 'Optional[int]'
  requestResponse: 'Optional[RequestResponse]'
  draftPayment: 'Optional[DraftPayment]'

from ..model.RequestResponse import RequestResponse
from ..model.DraftPayment import DraftPayment