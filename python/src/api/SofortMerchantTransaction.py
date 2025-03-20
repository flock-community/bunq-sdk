from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Amount import Amount
from .LabelMonetaryAccount import LabelMonetaryAccount
from .ErrorArray import ErrorArray

@dataclass
class SofortMerchantTransaction:
  amount_requested: Optional[Amount]
  issuer: Optional[str]
  monetary_account_id: Optional[int]
  alias: Optional[LabelMonetaryAccount]
  counterparty_alias: Optional[LabelMonetaryAccount]
  amount_guaranteed: Optional[Amount]
  issuer_authentication_url: Optional[str]
  status: Optional[str]
  error_message: Optional[List[List[ErrorArray]]]
  transaction_identifier: Optional[str]
