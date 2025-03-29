from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

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

from .Pointer import Pointer
from .Amount import Amount
from .MonetaryAccountProfile import MonetaryAccountProfile
from .MonetaryAccountSetting import MonetaryAccountSetting
from .MonetaryAccountBudget import MonetaryAccountBudget
from .ShareInviteMonetaryAccountResponse import ShareInviteMonetaryAccountResponse
from .BunqId import BunqId
from .Fulfillment import Fulfillment
from .RelationUser import RelationUser
from .CoOwner import CoOwner
from .CoOwnerInviteResponse import CoOwnerInviteResponse
from .OpenBankingAccount import OpenBankingAccount
from .BirdeeInvestmentPortfolio import BirdeeInvestmentPortfolio
from .MonetaryAccountLight import MonetaryAccountLight
from .MonetaryAccountBank import MonetaryAccountBank
from .MonetaryAccountExternal import MonetaryAccountExternal
from .MonetaryAccountInvestment import MonetaryAccountInvestment
from .MonetaryAccountJoint import MonetaryAccountJoint
from .MonetaryAccountSavings import MonetaryAccountSavings
from .MonetaryAccountSwitchService import MonetaryAccountSwitchService
from .MonetaryAccountExternalSavings import MonetaryAccountExternalSavings
from .MonetaryAccountCard import MonetaryAccountCard