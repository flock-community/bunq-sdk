from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Amount import Amount
from .AdditionalTransactionInformationCategory import AdditionalTransactionInformationCategory
from .UserPartnerPromotion import UserPartnerPromotion

@dataclass
class CashbackPayoutItem:
  status: Optional[str]
  amount: Optional[Amount]
  rate_applied: Optional[str]
  transaction_category: Optional[AdditionalTransactionInformationCategory]
  user_partner_promotion: Optional[UserPartnerPromotion]
