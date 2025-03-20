from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .LabelMonetaryAccount import LabelMonetaryAccount
from .Amount import Amount
from .LabelUser import LabelUser

@dataclass
class WhitelistSddRecurringRead:
  id: Optional[int]
  monetary_account_incoming_id: Optional[int]
  monetary_account_paying_id: Optional[int]
  type: Optional[str]
  status: Optional[str]
  credit_scheme_identifier: Optional[str]
  mandate_identifier: Optional[str]
  counterparty_alias: Optional[LabelMonetaryAccount]
  maximum_amount_per_month: Optional[Amount]
  maximum_amount_per_payment: Optional[Amount]
  user_alias_created: Optional[LabelUser]
  routing_type: Optional[str]
