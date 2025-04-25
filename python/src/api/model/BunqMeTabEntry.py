from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class BunqMeTabEntry:
  amount_inquired: 'Optional[Amount]'
  description: 'Optional[str]'
  redirect_url: 'Optional[str]'
  uuid: 'Optional[str]'
  alias: 'Optional[LabelMonetaryAccount]'
  status: 'Optional[str]'
  merchant_available: 'Optional[List[BunqMeMerchantAvailable]]'
  invite_profile_name: 'Optional[str]'

from ..model.Amount import Amount
from ..model.LabelMonetaryAccount import LabelMonetaryAccount
from ..model.BunqMeMerchantAvailable import BunqMeMerchantAvailable