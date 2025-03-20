from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .NotificationFilterUrl import NotificationFilterUrl

@dataclass
class NotificationFilterUrl:
  notification_filters: Optional[List[NotificationFilterUrl]]
