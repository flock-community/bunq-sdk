from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class MonetaryAccountRead:
  MonetaryAccountLight: 'Optional[MonetaryAccountLight]'
  MonetaryAccountBank: 'Optional[MonetaryAccountBank]'
  MonetaryAccountExternal: 'Optional[MonetaryAccountExternal]'
  MonetaryAccountInvestment: 'Optional[MonetaryAccountInvestment]'
  MonetaryAccountJoint: 'Optional[MonetaryAccountJoint]'
  MonetaryAccountSavings: 'Optional[MonetaryAccountSavings]'
  MonetaryAccountSwitchService: 'Optional[MonetaryAccountSwitchService]'
  MonetaryAccountExternalSavings: 'Optional[MonetaryAccountExternalSavings]'
  MonetaryAccountCard: 'Optional[MonetaryAccountCard]'

from ..model.MonetaryAccountLight import MonetaryAccountLight
from ..model.MonetaryAccountBank import MonetaryAccountBank
from ..model.MonetaryAccountExternal import MonetaryAccountExternal
from ..model.MonetaryAccountInvestment import MonetaryAccountInvestment
from ..model.MonetaryAccountJoint import MonetaryAccountJoint
from ..model.MonetaryAccountSavings import MonetaryAccountSavings
from ..model.MonetaryAccountSwitchService import MonetaryAccountSwitchService
from ..model.MonetaryAccountExternalSavings import MonetaryAccountExternalSavings
from ..model.MonetaryAccountCard import MonetaryAccountCard