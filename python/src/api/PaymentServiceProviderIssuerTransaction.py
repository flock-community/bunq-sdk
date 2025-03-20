from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Pointer import Pointer
from .Amount import Amount

@dataclass
class PaymentServiceProviderIssuerTransaction:
  counterparty_alias: Pointer
  amount: Amount
  description: str
  url_redirect: str
  time_expiry: Optional[str]
  status: Optional[str]
