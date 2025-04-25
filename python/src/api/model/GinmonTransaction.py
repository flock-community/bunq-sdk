from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class GinmonTransaction:
  status: 'Optional[str]'
  status_description: 'Optional[str]'
  status_description_translated: 'Optional[str]'
  amount_billing: 'Optional[Amount]'
  amount_billing_original: 'Optional[Amount]'
  isin: 'Optional[str]'
  external_identifier: 'Optional[str]'
  label_user: 'Optional[LabelUser]'
  label_monetary_account: 'Optional[LabelMonetaryAccount]'
  counter_label_monetary_account: 'Optional[LabelMonetaryAccount]'
  event_id: 'Optional[int]'

from ..model.Amount import Amount
from ..model.LabelUser import LabelUser
from ..model.LabelMonetaryAccount import LabelMonetaryAccount