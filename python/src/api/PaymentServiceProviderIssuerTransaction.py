from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class PaymentServiceProviderIssuerTransaction:
  counterparty_alias: 'Pointer'
  amount: 'Amount'
  description: 'str'
  url_redirect: 'str'
  time_expiry: 'Optional[str]'
  status: 'Optional[str]'

from .Pointer import Pointer
from .Amount import Amount