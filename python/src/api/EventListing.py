from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .EventObject import EventObject

@dataclass
class EventListing:
  id: Optional[int]
  created: Optional[str]
  updated: Optional[str]
  action: Optional[str]
  user_id: Optional[str]
  monetary_account_id: Optional[str]
  object: Optional[EventObject]
  status: Optional[str]
