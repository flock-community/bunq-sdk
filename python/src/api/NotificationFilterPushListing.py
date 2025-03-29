from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class NotificationFilterPushListing:
  notification_filters: 'Optional[List[NotificationFilterPush]]'

from .NotificationFilterPush import NotificationFilterPush