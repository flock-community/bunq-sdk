from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class ShareInviteMonetaryAccountResponseListing:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  counter_alias: 'Optional[LabelMonetaryAccount]'
  user_alias_cancelled: 'Optional[LabelUser]'
  monetary_account_id: 'Optional[int]'
  draft_share_invite_bank_id: 'Optional[int]'
  share_detail: 'Optional[ShareDetail]'
  access_type: 'Optional[str]'
  status: 'Optional[str]'
  relation_user: 'Optional[RelationUser]'
  share_type: 'Optional[str]'
  start_date: 'Optional[str]'
  end_date: 'Optional[str]'
  description: 'Optional[str]'

from ..model.LabelMonetaryAccount import LabelMonetaryAccount
from ..model.LabelUser import LabelUser
from ..model.ShareDetail import ShareDetail
from ..model.RelationUser import RelationUser