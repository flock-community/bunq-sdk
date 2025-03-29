from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class BunqMeFundraiserProfileUserListing:
  monetary_account_id: 'Optional[int]'
  owner_user_id: 'Optional[int]'
  color: 'Optional[str]'
  alias: 'Optional[LabelMonetaryAccount]'
  currency: 'Optional[str]'
  description: 'Optional[str]'
  attachment: 'Optional[AttachmentPublic]'
  pointer: 'Optional[Pointer]'
  redirect_url: 'Optional[str]'
  status: 'Optional[str]'

from .LabelMonetaryAccount import LabelMonetaryAccount
from .AttachmentPublic import AttachmentPublic
from .Pointer import Pointer