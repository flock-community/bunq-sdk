from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class NotificationFilterFailure:
  notification_filter_failed_ids: 'str'

