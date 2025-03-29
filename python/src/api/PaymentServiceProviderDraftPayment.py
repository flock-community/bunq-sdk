from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class PaymentServiceProviderDraftPayment:
  sender_iban: 'str'
  sender_name: 'Optional[str]'
  counterparty_iban: 'str'
  counterparty_name: 'str'
  description: 'str'
  amount: 'Amount'
  status: 'Optional[str]'

from .Amount import Amount