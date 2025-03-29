from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class ShareInviteMonetaryAccountResponse:
  status: 'Optional[str]'
  card_id: 'Optional[int]'
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  counter_alias: 'Optional[LabelMonetaryAccount]'
  user_alias_cancelled: 'Optional[LabelUser]'
  monetary_account_id: 'Optional[int]'
  draft_share_invite_bank_id: 'Optional[int]'
  share_detail: 'Optional[ShareDetail]'
  access_type: 'Optional[str]'
  relation_user: 'Optional[RelationUser]'
  share_type: 'Optional[str]'
  start_date: 'Optional[str]'
  end_date: 'Optional[str]'
  description: 'Optional[str]'

from .LabelMonetaryAccount import LabelMonetaryAccount
from .LabelUser import LabelUser
from .ShareDetail import ShareDetail
from .RelationUser import RelationUser