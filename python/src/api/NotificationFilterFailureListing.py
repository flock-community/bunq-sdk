from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .NotificationFilter import NotificationFilter

@dataclass
class NotificationFilterFailureListing:
  notification_filters: Optional[List[NotificationFilter]]
  category: Optional[str]
  event_type: Optional[str]
  object_id: Optional[int]
  exception_message: Optional[str]
  response_code: Optional[int]
