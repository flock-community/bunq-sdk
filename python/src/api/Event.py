from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .EventObject import EventObject

@dataclass
class Event:
  id: Optional[int]
  created: Optional[str]
  updated: Optional[str]
  action: Optional[str]
  user_id: Optional[str]
  monetary_account_id: Optional[str]
  object: Optional[EventObject]
  status: Optional[str]
  object_data_at_event: Optional[EventObject]
  is_event_latest_for_object: Optional[bool]
  is_event_reassignable: Optional[bool]
