from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class DraftPayment:
  status: 'Optional[str]'
  entries: 'List[DraftPaymentEntry]'
  previous_updated_timestamp: 'Optional[str]'
  number_of_required_accepts: 'int'
  schedule: 'Optional[Schedule]'

from .DraftPaymentEntry import DraftPaymentEntry
from .Schedule import Schedule