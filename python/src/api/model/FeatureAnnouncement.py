from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class FeatureAnnouncement:
  avatar: 'Optional[Avatar]'
  title: 'Optional[str]'
  sub_title: 'Optional[str]'
  type: 'Optional[str]'

from ..model.Avatar import Avatar