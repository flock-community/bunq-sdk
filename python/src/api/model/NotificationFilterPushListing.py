from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class NotificationFilterPushListing:
  notification_filters: 'Optional[List[NotificationFilterPush]]'

from ..model.NotificationFilterPush import NotificationFilterPush