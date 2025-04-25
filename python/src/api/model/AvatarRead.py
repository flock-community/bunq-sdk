from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class AvatarRead:
  uuid: 'Optional[str]'
  image: 'Optional[List[Image]]'

from ..model.Image import Image