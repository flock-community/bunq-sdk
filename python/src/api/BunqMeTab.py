from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class BunqMeTab:
  bunqme_tab_entry: 'BunqMeTabEntry'
  status: 'Optional[str]'
  event_id: 'Optional[int]'

from .BunqMeTabEntry import BunqMeTabEntry