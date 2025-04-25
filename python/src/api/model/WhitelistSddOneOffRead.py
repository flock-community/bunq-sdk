from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class WhitelistSddOneOffRead:
  id: 'Optional[int]'
  monetary_account_incoming_id: 'Optional[int]'
  monetary_account_paying_id: 'Optional[int]'
  type: 'Optional[str]'
  status: 'Optional[str]'
  credit_scheme_identifier: 'Optional[str]'
  counterparty_alias: 'Optional[LabelMonetaryAccount]'
  maximum_amount_per_month: 'Optional[Amount]'
  maximum_amount_per_payment: 'Optional[Amount]'
  user_alias_created: 'Optional[LabelUser]'
  routing_type: 'Optional[str]'

from ..model.LabelMonetaryAccount import LabelMonetaryAccount
from ..model.Amount import Amount
from ..model.LabelUser import LabelUser