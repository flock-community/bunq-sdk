from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .LabelMonetaryAccount import LabelMonetaryAccount
from .Amount import Amount

@dataclass
class PaymentServiceProviderIssuerTransactionRead:
  id: Optional[int]
  created: Optional[str]
  updated: Optional[str]
  public_uuid: Optional[str]
  counterparty_alias: Optional[LabelMonetaryAccount]
  amount: Optional[Amount]
  description: Optional[str]
  url_redirect: Optional[str]
  time_expiry: Optional[str]
  status: Optional[str]
  alias: Optional[LabelMonetaryAccount]
