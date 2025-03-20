from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class ShareDetailPayment:
  make_payments: Optional[bool]
  make_draft_payments: Optional[bool]
  view_balance: Optional[bool]
  view_old_events: Optional[bool]
  view_new_events: Optional[bool]
