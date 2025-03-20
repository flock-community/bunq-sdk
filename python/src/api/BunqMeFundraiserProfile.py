from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Pointer import Pointer
from .LabelMonetaryAccount import LabelMonetaryAccount
from .AttachmentPublic import AttachmentPublic
from .BunqMeMerchantAvailable import BunqMeMerchantAvailable

@dataclass
class BunqMeFundraiserProfile:
  pointer: Optional[Pointer]
  color: Optional[str]
  alias: Optional[LabelMonetaryAccount]
  currency: Optional[str]
  description: Optional[str]
  attachment: Optional[AttachmentPublic]
  status: Optional[str]
  redirect_url: Optional[str]
  invite_profile_name: Optional[str]
  merchant_available: Optional[List[BunqMeMerchantAvailable]]
