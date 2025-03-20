from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .BunqMeTabEntry import BunqMeTabEntry

@dataclass
class BunqMeTab:
  bunqme_tab_entry: BunqMeTabEntry
  status: Optional[str]
  event_id: Optional[int]
