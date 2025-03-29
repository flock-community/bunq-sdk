from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class AvatarRead:
  uuid: 'Optional[str]'
  image: 'Optional[List[Image]]'

from .Image import Image