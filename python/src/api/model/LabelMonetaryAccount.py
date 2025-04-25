from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class LabelMonetaryAccount:
  iban: 'Optional[str]'
  display_name: 'Optional[str]'
  avatar: 'Optional[Avatar]'
  label_user: 'Optional[LabelUser]'
  country: 'Optional[str]'
  bunq_me: 'Optional[Pointer]'
  is_light: 'Optional[bool]'
  swift_bic: 'Optional[str]'
  swift_account_number: 'Optional[str]'
  transferwise_account_number: 'Optional[str]'
  transferwise_bank_code: 'Optional[str]'
  merchant_category_code: 'Optional[str]'

from ..model.Avatar import Avatar
from ..model.LabelUser import LabelUser
from ..model.Pointer import Pointer