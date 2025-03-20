from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .LabelMonetaryAccount import LabelMonetaryAccount
from .Amount import Amount

@dataclass
class IdealMerchantTransactionListing:
  monetary_account_id: Optional[int]
  alias: Optional[LabelMonetaryAccount]
  counterparty_alias: Optional[LabelMonetaryAccount]
  amount_guaranteed: Optional[Amount]
  amount_requested: Optional[Amount]
  expiration: Optional[str]
  issuer: Optional[str]
  issuer_name: Optional[str]
  issuer_authentication_url: Optional[str]
  purchase_identifier: Optional[str]
  status: Optional[str]
  status_timestamp: Optional[str]
  transaction_identifier: Optional[str]
