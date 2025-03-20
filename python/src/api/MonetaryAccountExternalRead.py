from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Avatar import Avatar
from .Amount import Amount
from .Pointer import Pointer
from .MonetaryAccountProfile import MonetaryAccountProfile
from .MonetaryAccountSetting import MonetaryAccountSetting
from .BunqId import BunqId
from .OpenBankingAccount import OpenBankingAccount

@dataclass
class MonetaryAccountExternalRead:
  id: Optional[int]
  created: Optional[str]
  updated: Optional[str]
  avatar: Optional[Avatar]
  currency: Optional[str]
  description: Optional[str]
  daily_limit: Optional[Amount]
  overdraft_limit: Optional[Amount]
  balance: Optional[Amount]
  alias: Optional[List[Pointer]]
  public_uuid: Optional[str]
  status: Optional[str]
  sub_status: Optional[str]
  reason: Optional[str]
  reason_description: Optional[str]
  user_id: Optional[int]
  monetary_account_profile: Optional[MonetaryAccountProfile]
  display_name: Optional[str]
  setting: Optional[MonetaryAccountSetting]
  all_auto_save_id: Optional[List[BunqId]]
  service: Optional[str]
  open_banking_account: Optional[OpenBankingAccount]
