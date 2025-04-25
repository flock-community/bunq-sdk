from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class DraftPaymentEntry:
  amount: 'Optional[Amount]'
  counterparty_alias: 'Optional[LabelMonetaryAccount]'
  description: 'Optional[str]'
  merchant_reference: 'Optional[str]'
  attachment: 'Optional[List[AttachmentMonetaryAccountPayment]]'
  id: 'Optional[int]'
  alias: 'Optional[LabelMonetaryAccount]'
  type: 'Optional[str]'

from ..model.Amount import Amount
from ..model.LabelMonetaryAccount import LabelMonetaryAccount
from ..model.AttachmentMonetaryAccountPayment import AttachmentMonetaryAccountPayment