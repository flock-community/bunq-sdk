from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class DraftPayment:
  status: 'Optional[str]'
  entries: 'List[DraftPaymentEntry]'
  previous_updated_timestamp: 'Optional[str]'
  number_of_required_accepts: 'int'
  schedule: 'Optional[Schedule]'

from ..model.DraftPaymentEntry import DraftPaymentEntry
from ..model.Schedule import Schedule