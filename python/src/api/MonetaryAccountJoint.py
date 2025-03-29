from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class MonetaryAccountJoint:
  currency: 'Optional[str]'
  description: 'Optional[str]'
  daily_limit: 'Optional[Amount]'
  overdraft_limit: 'Optional[Amount]'
  alias: 'Optional[List[Pointer]]'
  avatar_uuid: 'Optional[str]'
  status: 'Optional[str]'
  sub_status: 'Optional[str]'
  reason: 'Optional[str]'
  reason_description: 'Optional[str]'
  all_co_owner: 'Optional[List[CoOwner]]'
  setting: 'Optional[MonetaryAccountSetting]'
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  avatar: 'Optional[Avatar]'
  balance: 'Optional[Amount]'
  public_uuid: 'Optional[str]'
  user_id: 'Optional[int]'
  monetary_account_profile: 'Optional[MonetaryAccountProfile]'
  all_auto_save_id: 'Optional[List[BunqId]]'

from .Amount import Amount
from .Pointer import Pointer
from .CoOwner import CoOwner
from .MonetaryAccountSetting import MonetaryAccountSetting
from .Avatar import Avatar
from .MonetaryAccountProfile import MonetaryAccountProfile
from .BunqId import BunqId