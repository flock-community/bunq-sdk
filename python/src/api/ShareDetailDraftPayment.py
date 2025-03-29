from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class ShareDetailDraftPayment:
  make_draft_payments: 'Optional[bool]'
  view_balance: 'Optional[bool]'
  view_old_events: 'Optional[bool]'
  view_new_events: 'Optional[bool]'

