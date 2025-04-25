from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class BunqMeFundraiserProfile:
  pointer: 'Optional[Pointer]'
  color: 'Optional[str]'
  alias: 'Optional[LabelMonetaryAccount]'
  currency: 'Optional[str]'
  description: 'Optional[str]'
  attachment: 'Optional[AttachmentPublic]'
  status: 'Optional[str]'
  redirect_url: 'Optional[str]'
  invite_profile_name: 'Optional[str]'
  merchant_available: 'Optional[List[BunqMeMerchantAvailable]]'

from ..model.Pointer import Pointer
from ..model.LabelMonetaryAccount import LabelMonetaryAccount
from ..model.AttachmentPublic import AttachmentPublic
from ..model.BunqMeMerchantAvailable import BunqMeMerchantAvailable