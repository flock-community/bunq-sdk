from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class IdealMerchantTransaction:
  amount_requested: 'Optional[Amount]'
  issuer: 'Optional[str]'
  monetary_account_id: 'Optional[int]'
  alias: 'Optional[LabelMonetaryAccount]'
  counterparty_alias: 'Optional[LabelMonetaryAccount]'
  amount_guaranteed: 'Optional[Amount]'
  expiration: 'Optional[str]'
  issuer_name: 'Optional[str]'
  issuer_authentication_url: 'Optional[str]'
  purchase_identifier: 'Optional[str]'
  status: 'Optional[str]'
  status_timestamp: 'Optional[str]'
  transaction_identifier: 'Optional[str]'

from .Amount import Amount
from .LabelMonetaryAccount import LabelMonetaryAccount