from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class TransferwiseTransfer:
  monetary_account_id: 'str'
  recipient_id: 'str'
  alias: 'Optional[LabelMonetaryAccount]'
  counterparty_alias: 'Optional[LabelMonetaryAccount]'
  status: 'Optional[str]'
  sub_status: 'Optional[str]'
  status_transferwise: 'Optional[str]'
  status_transferwise_issue: 'Optional[str]'
  amount_source: 'Optional[Amount]'
  amount_target: 'Optional[Amount]'
  rate: 'Optional[str]'
  reference: 'Optional[str]'
  pay_in_reference: 'Optional[str]'
  time_delivery_estimate: 'Optional[str]'
  quote: 'Optional[TransferwiseQuote]'

from ..model.LabelMonetaryAccount import LabelMonetaryAccount
from ..model.Amount import Amount
from ..model.TransferwiseQuote import TransferwiseQuote