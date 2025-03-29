from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class NotificationFilter:
  notification_delivery_method: 'Optional[str]'
  notification_target: 'Optional[str]'
  category: 'Optional[str]'

