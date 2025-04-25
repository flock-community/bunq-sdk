from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class BunqMeTab:
  bunqme_tab_entry: 'BunqMeTabEntry'
  status: 'Optional[str]'
  event_id: 'Optional[int]'

from ..model.BunqMeTabEntry import BunqMeTabEntry