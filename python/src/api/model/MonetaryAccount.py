from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class MonetaryAccount:
  alias: 'Optional[List[Pointer]]'
  balance: 'Optional[Amount]'
  monetary_account_profile: 'Optional[List[MonetaryAccountProfile]]'
  setting: 'Optional[MonetaryAccountSetting]'
  budget: 'Optional[List[MonetaryAccountBudget]]'
  reason: 'Optional[str]'
  reason_description: 'Optional[str]'
  share: 'Optional[ShareInviteMonetaryAccountResponse]'
  all_auto_save_id: 'Optional[List[BunqId]]'
  fulfillments: 'Optional[List[Fulfillment]]'
  relation_user: 'Optional[RelationUser]'
  all_co_owner: 'Optional[List[CoOwner]]'
  co_owner_invite: 'Optional[CoOwnerInviteResponse]'
  open_banking_account: 'Optional[OpenBankingAccount]'
  birdee_investment_portfolio: 'Optional[BirdeeInvestmentPortfolio]'
  MonetaryAccountLight: 'Optional[MonetaryAccountLight]'
  MonetaryAccountBank: 'Optional[MonetaryAccountBank]'
  MonetaryAccountExternal: 'Optional[MonetaryAccountExternal]'
  MonetaryAccountInvestment: 'Optional[MonetaryAccountInvestment]'
  MonetaryAccountJoint: 'Optional[MonetaryAccountJoint]'
  MonetaryAccountSavings: 'Optional[MonetaryAccountSavings]'
  MonetaryAccountSwitchService: 'Optional[MonetaryAccountSwitchService]'
  MonetaryAccountExternalSavings: 'Optional[MonetaryAccountExternalSavings]'
  MonetaryAccountCard: 'Optional[MonetaryAccountCard]'

from ..model.Pointer import Pointer
from ..model.Amount import Amount
from ..model.MonetaryAccountProfile import MonetaryAccountProfile
from ..model.MonetaryAccountSetting import MonetaryAccountSetting
from ..model.MonetaryAccountBudget import MonetaryAccountBudget
from ..model.ShareInviteMonetaryAccountResponse import ShareInviteMonetaryAccountResponse
from ..model.BunqId import BunqId
from ..model.Fulfillment import Fulfillment
from ..model.RelationUser import RelationUser
from ..model.CoOwner import CoOwner
from ..model.CoOwnerInviteResponse import CoOwnerInviteResponse
from ..model.OpenBankingAccount import OpenBankingAccount
from ..model.BirdeeInvestmentPortfolio import BirdeeInvestmentPortfolio
from ..model.MonetaryAccountLight import MonetaryAccountLight
from ..model.MonetaryAccountBank import MonetaryAccountBank
from ..model.MonetaryAccountExternal import MonetaryAccountExternal
from ..model.MonetaryAccountInvestment import MonetaryAccountInvestment
from ..model.MonetaryAccountJoint import MonetaryAccountJoint
from ..model.MonetaryAccountSavings import MonetaryAccountSavings
from ..model.MonetaryAccountSwitchService import MonetaryAccountSwitchService
from ..model.MonetaryAccountExternalSavings import MonetaryAccountExternalSavings
from ..model.MonetaryAccountCard import MonetaryAccountCard