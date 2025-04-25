from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class MonetaryAccountInvestment:
  currency: 'Optional[str]'
  provider: 'str'
  description: 'Optional[str]'
  daily_limit: 'Optional[Amount]'
  avatar_uuid: 'Optional[str]'
  status: 'Optional[str]'
  sub_status: 'Optional[str]'
  reason: 'Optional[str]'
  reason_description: 'Optional[str]'
  display_name: 'Optional[str]'
  setting: 'Optional[MonetaryAccountSetting]'
  birdee_investment_portfolio: 'Optional[BirdeeInvestmentPortfolio]'
  monetary_account_deposit_initial_id: 'Optional[int]'
  amount_deposit_initial: 'Optional[Amount]'
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  avatar: 'Optional[Avatar]'
  balance: 'Optional[Amount]'
  alias: 'Optional[List[Pointer]]'
  public_uuid: 'Optional[str]'
  user_id: 'Optional[int]'
  monetary_account_profile: 'Optional[MonetaryAccountProfile]'
  all_auto_save_id: 'Optional[List[BunqId]]'

from ..model.Amount import Amount
from ..model.MonetaryAccountSetting import MonetaryAccountSetting
from ..model.BirdeeInvestmentPortfolio import BirdeeInvestmentPortfolio
from ..model.Avatar import Avatar
from ..model.Pointer import Pointer
from ..model.MonetaryAccountProfile import MonetaryAccountProfile
from ..model.BunqId import BunqId