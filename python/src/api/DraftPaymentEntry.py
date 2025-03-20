from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Amount import Amount
from .LabelMonetaryAccount import LabelMonetaryAccount
from .AttachmentMonetaryAccountPayment import AttachmentMonetaryAccountPayment

@dataclass
class DraftPaymentEntry:
  amount: Optional[Amount]
  counterparty_alias: Optional[LabelMonetaryAccount]
  description: Optional[str]
  merchant_reference: Optional[str]
  attachment: Optional[List[AttachmentMonetaryAccountPayment]]
  id: Optional[int]
  alias: Optional[LabelMonetaryAccount]
  type: Optional[str]
