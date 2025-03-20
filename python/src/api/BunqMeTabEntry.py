from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Amount import Amount
from .LabelMonetaryAccount import LabelMonetaryAccount
from .BunqMeMerchantAvailable import BunqMeMerchantAvailable

@dataclass
class BunqMeTabEntry:
  amount_inquired: Optional[Amount]
  description: Optional[str]
  redirect_url: Optional[str]
  uuid: Optional[str]
  alias: Optional[LabelMonetaryAccount]
  status: Optional[str]
  merchant_available: Optional[List[BunqMeMerchantAvailable]]
  invite_profile_name: Optional[str]
