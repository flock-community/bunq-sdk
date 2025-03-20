from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Amount import Amount
from .MonetaryAccountSetting import MonetaryAccountSetting
from .Avatar import Avatar
from .Pointer import Pointer
from .MonetaryAccountProfile import MonetaryAccountProfile
from .BunqId import BunqId
from .OpenBankingAccount import OpenBankingAccount

@dataclass
class MonetaryAccountExternal:
  currency: Optional[str]
  service: Optional[str]
  description: Optional[str]
  daily_limit: Optional[Amount]
  avatar_uuid: Optional[str]
  status: Optional[str]
  sub_status: Optional[str]
  reason: Optional[str]
  reason_description: Optional[str]
  display_name: Optional[str]
  setting: Optional[MonetaryAccountSetting]
  id: Optional[int]
  created: Optional[str]
  updated: Optional[str]
  avatar: Optional[Avatar]
  overdraft_limit: Optional[Amount]
  balance: Optional[Amount]
  alias: Optional[List[Pointer]]
  public_uuid: Optional[str]
  user_id: Optional[int]
  monetary_account_profile: Optional[MonetaryAccountProfile]
  all_auto_save_id: Optional[List[BunqId]]
  open_banking_account: Optional[OpenBankingAccount]
