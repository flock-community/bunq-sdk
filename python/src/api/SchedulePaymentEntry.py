from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Amount import Amount
from .LabelMonetaryAccount import LabelMonetaryAccount
from .AttachmentMonetaryAccountPayment import AttachmentMonetaryAccountPayment

@dataclass
class SchedulePaymentEntry:
  amount: Optional[Amount]
  counterparty_alias: Optional[LabelMonetaryAccount]
  description: Optional[str]
  attachment: Optional[List[AttachmentMonetaryAccountPayment]]
  merchant_reference: Optional[str]
  allow_bunqto: Optional[bool]
  alias: Optional[LabelMonetaryAccount]
