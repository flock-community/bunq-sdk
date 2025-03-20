from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .DraftPaymentEntry import DraftPaymentEntry
from .Schedule import Schedule

@dataclass
class DraftPayment:
  status: Optional[str]
  entries: List[DraftPaymentEntry]
  previous_updated_timestamp: Optional[str]
  number_of_required_accepts: int
  schedule: Optional[Schedule]
