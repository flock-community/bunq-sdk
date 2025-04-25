from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class NotificationFilterUrl:
  notification_filters: 'Optional[List[NotificationFilterUrl]]'

