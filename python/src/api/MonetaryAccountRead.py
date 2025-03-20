from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .MonetaryAccountLight import MonetaryAccountLight
from .MonetaryAccountBank import MonetaryAccountBank
from .MonetaryAccountExternal import MonetaryAccountExternal
from .MonetaryAccountInvestment import MonetaryAccountInvestment
from .MonetaryAccountJoint import MonetaryAccountJoint
from .MonetaryAccountSavings import MonetaryAccountSavings
from .MonetaryAccountSwitchService import MonetaryAccountSwitchService
from .MonetaryAccountExternalSavings import MonetaryAccountExternalSavings
from .MonetaryAccountCard import MonetaryAccountCard

@dataclass
class MonetaryAccountRead:
  MonetaryAccountLight: Optional[MonetaryAccountLight]
  MonetaryAccountBank: Optional[MonetaryAccountBank]
  MonetaryAccountExternal: Optional[MonetaryAccountExternal]
  MonetaryAccountInvestment: Optional[MonetaryAccountInvestment]
  MonetaryAccountJoint: Optional[MonetaryAccountJoint]
  MonetaryAccountSavings: Optional[MonetaryAccountSavings]
  MonetaryAccountSwitchService: Optional[MonetaryAccountSwitchService]
  MonetaryAccountExternalSavings: Optional[MonetaryAccountExternalSavings]
  MonetaryAccountCard: Optional[MonetaryAccountCard]
