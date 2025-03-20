from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .PartnerPromotionCashback import PartnerPromotionCashback

@dataclass
class UserPartnerPromotion:
  promotion_code: str
  status: Optional[str]
  number_of_transaction_remaining: Optional[int]
  partner_promotion: Optional[PartnerPromotionCashback]
