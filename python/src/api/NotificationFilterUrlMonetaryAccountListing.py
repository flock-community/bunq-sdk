from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class NotificationFilterUrlMonetaryAccountListing:
  notification_filters: 'Optional[List[NotificationFilterUrl]]'

from .NotificationFilterUrl import NotificationFilterUrl