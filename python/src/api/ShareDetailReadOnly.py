from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class ShareDetailReadOnly:
  view_balance: Optional[bool]
  view_old_events: Optional[bool]
  view_new_events: Optional[bool]
