from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class MonetaryAccountSavingsRead:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  avatar: 'Optional[Avatar]'
  currency: 'Optional[str]'
  description: 'Optional[str]'
  daily_limit: 'Optional[Amount]'
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
  savings_goal: 'Optional[Amount]'
  savings_goal_progress: 'Optional[int]'
  number_of_payment_remaining: 'Optional[str]'
  all_auto_save_id: 'Optional[List[BunqId]]'

from .Avatar import Avatar
from .Amount import Amount
from .Pointer import Pointer
from .CoOwner import CoOwner
from .MonetaryAccountProfile import MonetaryAccountProfile
from .MonetaryAccountSetting import MonetaryAccountSetting
from .BunqId import BunqId