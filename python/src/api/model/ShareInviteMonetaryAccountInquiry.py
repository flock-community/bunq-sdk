from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class ShareInviteMonetaryAccountInquiry:
  counter_user_alias: 'Optional[LabelUser]'
  access_type: 'Optional[str]'
  draft_share_invite_bank_id: 'Optional[int]'
  share_detail: 'Optional[ShareDetail]'
  status: 'Optional[str]'
  relationship: 'Optional[str]'
  share_type: 'Optional[str]'
  start_date: 'Optional[str]'
  end_date: 'Optional[str]'
  alias: 'Optional[LabelMonetaryAccount]'
  user_alias_created: 'Optional[LabelUser]'
  user_alias_revoked: 'Optional[LabelUser]'
  monetary_account_id: 'Optional[int]'
  id: 'Optional[int]'

from ..model.LabelUser import LabelUser
from ..model.ShareDetail import ShareDetail
from ..model.LabelMonetaryAccount import LabelMonetaryAccount