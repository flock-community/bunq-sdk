from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Image import Image

@dataclass
class AvatarRead:
  uuid: Optional[str]
  image: Optional[List[Image]]
