from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class MonetaryAccountLight:
  currency: 'Optional[str]'
  description: 'Optional[str]'
  daily_limit: 'Optional[Amount]'
  avatar_uuid: 'Optional[str]'
  status: 'Optional[str]'
  sub_status: 'Optional[str]'
  reason: 'Optional[str]'
  reason_description: 'Optional[str]'
  setting: 'Optional[MonetaryAccountSetting]'
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  avatar: 'Optional[Avatar]'
  balance: 'Optional[Amount]'
  alias: 'Optional[List[Pointer]]'
  public_uuid: 'Optional[str]'
  user_id: 'Optional[int]'
  balance_maximum: 'Optional[Amount]'
  budget_month_used: 'Optional[Amount]'
  budget_month_maximum: 'Optional[Amount]'
  budget_year_used: 'Optional[Amount]'
  budget_year_maximum: 'Optional[Amount]'
  budget_withdrawal_year_used: 'Optional[Amount]'
  budget_withdrawal_year_maximum: 'Optional[Amount]'

from .Amount import Amount
from .MonetaryAccountSetting import MonetaryAccountSetting
from .Avatar import Avatar
from .Pointer import Pointer