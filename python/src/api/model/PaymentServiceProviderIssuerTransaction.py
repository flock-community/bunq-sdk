from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class PaymentServiceProviderIssuerTransaction:
  counterparty_alias: 'Pointer'
  amount: 'Amount'
  description: 'str'
  url_redirect: 'str'
  time_expiry: 'Optional[str]'
  status: 'Optional[str]'

from ..model.Pointer import Pointer
from ..model.Amount import Amount