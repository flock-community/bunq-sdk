from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class PartnerPromotionCashback:
  promotion_code: 'Optional[str]'
  status: 'Optional[str]'
  description: 'str'
  date_start: 'str'
  date_end: 'str'
  currency: 'str'
  amount_cashback_per_transaction_maximum: 'Optional[Amount]'
  number_of_transaction_maximum: 'Optional[int]'
  amount_transaction_minimum: 'Optional[Amount]'
  url_together: 'Optional[str]'
  deeplink: 'Optional[str]'
  partner_name: 'Optional[str]'
  partner_avatar_uuid: 'str'
  promotion_title_short: 'Optional[StringTranslated]'
  promotion_title_long: 'Optional[StringTranslated]'
  promotion_description: 'Optional[StringTranslated]'
  all_partner_identifier: 'Optional[List[str]]'
  public_uuid: 'Optional[str]'
  partner_avatar: 'Optional[Avatar]'

from ..model.Amount import Amount
from ..model.StringTranslated import StringTranslated
from ..model.Avatar import Avatar