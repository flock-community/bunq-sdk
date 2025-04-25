from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class MonetaryAccountExternal:
  currency: 'Optional[str]'
  service: 'Optional[str]'
  description: 'Optional[str]'
  daily_limit: 'Optional[Amount]'
  avatar_uuid: 'Optional[str]'
  status: 'Optional[str]'
  sub_status: 'Optional[str]'
  reason: 'Optional[str]'
  reason_description: 'Optional[str]'
  display_name: 'Optional[str]'
  setting: 'Optional[MonetaryAccountSetting]'
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  avatar: 'Optional[Avatar]'
  overdraft_limit: 'Optional[Amount]'
  balance: 'Optional[Amount]'
  alias: 'Optional[List[Pointer]]'
  public_uuid: 'Optional[str]'
  user_id: 'Optional[int]'
  monetary_account_profile: 'Optional[MonetaryAccountProfile]'
  all_auto_save_id: 'Optional[List[BunqId]]'
  open_banking_account: 'Optional[OpenBankingAccount]'

from ..model.Amount import Amount
from ..model.MonetaryAccountSetting import MonetaryAccountSetting
from ..model.Avatar import Avatar
from ..model.Pointer import Pointer
from ..model.MonetaryAccountProfile import MonetaryAccountProfile
from ..model.BunqId import BunqId
from ..model.OpenBankingAccount import OpenBankingAccount