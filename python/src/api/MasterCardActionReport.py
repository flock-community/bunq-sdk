from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .LabelMonetaryAccount import LabelMonetaryAccount

@dataclass
class MasterCardActionReport:
  mastercard_action_id: Optional[int]
  type: Optional[str]
  status: Optional[str]
  merchant_id: Optional[str]
  merchant_name: Optional[str]
  counterparty_alias: Optional[LabelMonetaryAccount]
