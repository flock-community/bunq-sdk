from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class AttachmentUrl:
  type: Optional[str]
  url: Optional[str]
