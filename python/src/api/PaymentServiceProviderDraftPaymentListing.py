from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class PaymentServiceProviderDraftPaymentListing:
  sender_iban: 'Optional[str]'
  receiver_iban: 'Optional[str]'
  amount: 'Optional[Amount]'
  status: 'Optional[str]'

from .Amount import Amount