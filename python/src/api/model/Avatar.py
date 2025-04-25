from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class Avatar:
  uuid: 'Optional[str]'
  anchor_uuid: 'Optional[str]'
  image: 'Optional[List[Image]]'
  style: 'Optional[str]'

from ..model.Image import Image