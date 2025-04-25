from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class MonetaryAccountJointListing:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  avatar: 'Optional[Avatar]'
  currency: 'Optional[str]'
  description: 'Optional[str]'
  daily_limit: 'Optional[Amount]'
  overdraft_limit: 'Optional[Amount]'
  balance: 'Optional[Amount]'
  alias: 'Optional[List[Pointer]]'
  public_uuid: 'Optional[str]'
  status: 'Optional[str]'
  sub_status: 'Optional[str]'
  reason: 'Optional[str]'
  reason_description: 'Optional[str]'
  all_co_owner: 'Optional[List[CoOwner]]'
  user_id: 'Optional[int]'
  monetary_account_profile: 'Optional[MonetaryAccountProfile]'
  setting: 'Optional[MonetaryAccountSetting]'
  all_auto_save_id: 'Optional[List[BunqId]]'

from ..model.Avatar import Avatar
from ..model.Amount import Amount
from ..model.Pointer import Pointer
from ..model.CoOwner import CoOwner
from ..model.MonetaryAccountProfile import MonetaryAccountProfile
from ..model.MonetaryAccountSetting import MonetaryAccountSetting
from ..model.BunqId import BunqId