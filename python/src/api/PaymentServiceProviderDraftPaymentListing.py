from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Amount import Amount

@dataclass
class PaymentServiceProviderDraftPaymentListing:
  sender_iban: Optional[str]
  receiver_iban: Optional[str]
  amount: Optional[Amount]
  status: Optional[str]
