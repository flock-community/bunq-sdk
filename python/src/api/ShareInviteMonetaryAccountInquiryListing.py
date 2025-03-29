from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class ShareInviteMonetaryAccountInquiryListing:
  alias: 'Optional[LabelMonetaryAccount]'
  user_alias_created: 'Optional[LabelUser]'
  user_alias_revoked: 'Optional[LabelUser]'
  counter_user_alias: 'Optional[LabelUser]'
  monetary_account_id: 'Optional[int]'
  status: 'Optional[str]'
  access_type: 'Optional[str]'
  relationship: 'Optional[str]'
  id: 'Optional[int]'

from .LabelMonetaryAccount import LabelMonetaryAccount
from .LabelUser import LabelUser