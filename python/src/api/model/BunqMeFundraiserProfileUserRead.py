from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class BunqMeFundraiserProfileUserRead:
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

from ..model.LabelMonetaryAccount import LabelMonetaryAccount
from ..model.AttachmentPublic import AttachmentPublic
from ..model.Pointer import Pointer