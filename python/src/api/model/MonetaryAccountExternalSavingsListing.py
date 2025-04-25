from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class MonetaryAccountExternalSavingsListing:
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
  user_id: 'Optional[int]'
  monetary_account_profile: 'Optional[MonetaryAccountProfile]'
  display_name: 'Optional[str]'
  setting: 'Optional[MonetaryAccountSetting]'
  all_auto_save_id: 'Optional[List[BunqId]]'
  savings_goal: 'Optional[Amount]'
  savings_goal_progress: 'Optional[int]'
  number_of_payment_remaining: 'Optional[str]'

from ..model.Avatar import Avatar
from ..model.Amount import Amount
from ..model.Pointer import Pointer
from ..model.MonetaryAccountProfile import MonetaryAccountProfile
from ..model.MonetaryAccountSetting import MonetaryAccountSetting
from ..model.BunqId import BunqId