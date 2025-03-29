from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class BankSwitchServiceNetherlandsIncoming:
  alias: 'Optional[LabelMonetaryAccount]'
  counterparty_alias: 'Optional[LabelMonetaryAccount]'
  status: 'Optional[str]'
  user_alias: 'Optional[LabelUser]'
  sub_status: 'Optional[str]'
  time_start_desired: 'Optional[str]'
  time_start_actual: 'Optional[str]'
  time_end: 'Optional[str]'
  attachment: 'Optional[Attachment]'
  rejection_reason: 'Optional[str]'
  rejection_reason_description: 'Optional[str]'
  rejection_reason_description_translated: 'Optional[str]'
  rejection_reason_together_url: 'Optional[str]'

from .LabelMonetaryAccount import LabelMonetaryAccount
from .LabelUser import LabelUser
from .Attachment import Attachment