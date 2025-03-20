from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .NotificationFilterEmail import NotificationFilterEmail

@dataclass
class NotificationFilterEmail:
  notification_filters: Optional[List[NotificationFilterEmail]]
