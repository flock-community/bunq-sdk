from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class SofortMerchantTransaction:
  amount_requested: 'Optional[Amount]'
  issuer: 'Optional[str]'
  monetary_account_id: 'Optional[int]'
  alias: 'Optional[LabelMonetaryAccount]'
  counterparty_alias: 'Optional[LabelMonetaryAccount]'
  amount_guaranteed: 'Optional[Amount]'
  issuer_authentication_url: 'Optional[str]'
  status: 'Optional[str]'
  error_message: 'Optional[List[List[ErrorArray]]]'
  transaction_identifier: 'Optional[str]'

from ..model.Amount import Amount
from ..model.LabelMonetaryAccount import LabelMonetaryAccount
from ..model.ErrorArray import ErrorArray