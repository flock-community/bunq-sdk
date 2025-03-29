from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class Avatar:
  uuid: 'Optional[str]'
  anchor_uuid: 'Optional[str]'
  image: 'Optional[List[Image]]'
  style: 'Optional[str]'

from .Image import Image