from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class NotificationFilter:
  notification_delivery_method: Optional[str]
  notification_target: Optional[str]
  category: Optional[str]
