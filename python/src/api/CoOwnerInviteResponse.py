from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .LabelMonetaryAccount import LabelMonetaryAccount
from .LabelUser import LabelUser
from .CoOwner import CoOwner

@dataclass
class CoOwnerInviteResponse:
  status: Optional[str]
  alias: Optional[LabelMonetaryAccount]
  counter_alias: Optional[LabelMonetaryAccount]
  monetary_account_id: Optional[int]
  monetary_account_type: Optional[str]
  freeze_status: Optional[str]
  label_freeze_user: Optional[LabelUser]
  all_co_owner: Optional[List[CoOwner]]
