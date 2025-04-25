from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class CashbackPayoutItem:
  status: 'Optional[str]'
  amount: 'Optional[Amount]'
  rate_applied: 'Optional[str]'
  transaction_category: 'Optional[AdditionalTransactionInformationCategory]'
  user_partner_promotion: 'Optional[UserPartnerPromotion]'

from ..model.Amount import Amount
from ..model.AdditionalTransactionInformationCategory import AdditionalTransactionInformationCategory
from ..model.UserPartnerPromotion import UserPartnerPromotion