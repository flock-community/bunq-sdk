from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class NotificationFilterEmailListing:
  notification_filters: 'Optional[List[NotificationFilterEmail]]'

from ..model.NotificationFilterEmail import NotificationFilterEmail