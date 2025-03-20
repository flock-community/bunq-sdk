from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .BankSwitchServiceNetherlandsIncoming import BankSwitchServiceNetherlandsIncoming
from .Payment import Payment

@dataclass
class BankSwitchServiceNetherlandsIncomingPayment:
  bank_switch_service: Optional[BankSwitchServiceNetherlandsIncoming]
  payment: Optional[Payment]
