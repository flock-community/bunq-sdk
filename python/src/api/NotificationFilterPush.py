from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .NotificationFilterPush import NotificationFilterPush

@dataclass
class NotificationFilterPush:
  notification_filters: Optional[List[NotificationFilterPush]]
