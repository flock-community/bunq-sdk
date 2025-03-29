from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class SofortMerchantTransactionListing:
  monetary_account_id: 'Optional[int]'
  alias: 'Optional[LabelMonetaryAccount]'
  counterparty_alias: 'Optional[LabelMonetaryAccount]'
  amount_guaranteed: 'Optional[Amount]'
  amount_requested: 'Optional[Amount]'
  issuer: 'Optional[str]'
  issuer_authentication_url: 'Optional[str]'
  status: 'Optional[str]'
  error_message: 'Optional[List[List[ErrorArray]]]'
  transaction_identifier: 'Optional[str]'

from .LabelMonetaryAccount import LabelMonetaryAccount
from .Amount import Amount
from .ErrorArray import ErrorArray