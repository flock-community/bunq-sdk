from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class EventRead:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  action: 'Optional[str]'
  user_id: 'Optional[str]'
  monetary_account_id: 'Optional[str]'
  object: 'Optional[EventObject]'
  status: 'Optional[str]'

from ..model.EventObject import EventObject