from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Amount import Amount

@dataclass
class PaymentServiceProviderDraftPayment:
  sender_iban: str
  sender_name: Optional[str]
  counterparty_iban: str
  counterparty_name: str
  description: str
  amount: Amount
  status: Optional[str]
