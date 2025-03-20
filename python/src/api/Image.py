from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class Image:
  attachment_public_uuid: Optional[str]
  content_type: Optional[str]
  height: Optional[int]
  width: Optional[int]
