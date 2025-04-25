from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class SchedulePaymentEntry:
  amount: 'Optional[Amount]'
  counterparty_alias: 'Optional[LabelMonetaryAccount]'
  description: 'Optional[str]'
  attachment: 'Optional[List[AttachmentMonetaryAccountPayment]]'
  merchant_reference: 'Optional[str]'
  allow_bunqto: 'Optional[bool]'
  alias: 'Optional[LabelMonetaryAccount]'

from ..model.Amount import Amount
from ..model.LabelMonetaryAccount import LabelMonetaryAccount
from ..model.AttachmentMonetaryAccountPayment import AttachmentMonetaryAccountPayment