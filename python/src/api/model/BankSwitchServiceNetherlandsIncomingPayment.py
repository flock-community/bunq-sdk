from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class BankSwitchServiceNetherlandsIncomingPayment:
  bank_switch_service: 'Optional[BankSwitchServiceNetherlandsIncoming]'
  payment: 'Optional[Payment]'

from ..model.BankSwitchServiceNetherlandsIncoming import BankSwitchServiceNetherlandsIncoming
from ..model.Payment import Payment