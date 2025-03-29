from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class BankSwitchServiceNetherlandsIncomingPayment:
  bank_switch_service: 'Optional[BankSwitchServiceNetherlandsIncoming]'
  payment: 'Optional[Payment]'

from .BankSwitchServiceNetherlandsIncoming import BankSwitchServiceNetherlandsIncoming
from .Payment import Payment