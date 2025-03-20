from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Image import Image

@dataclass
class Avatar:
  uuid: Optional[str]
  anchor_uuid: Optional[str]
  image: Optional[List[Image]]
  style: Optional[str]
