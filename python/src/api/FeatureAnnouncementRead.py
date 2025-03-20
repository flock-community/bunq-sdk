from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Avatar import Avatar

@dataclass
class FeatureAnnouncementRead:
  avatar: Optional[Avatar]
  title: Optional[str]
  sub_title: Optional[str]
  type: Optional[str]
