from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class MasterCardActionReport:
  mastercard_action_id: 'Optional[int]'
  type: 'Optional[str]'
  status: 'Optional[str]'
  merchant_id: 'Optional[str]'
  merchant_name: 'Optional[str]'
  counterparty_alias: 'Optional[LabelMonetaryAccount]'

from ..model.LabelMonetaryAccount import LabelMonetaryAccount