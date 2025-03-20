from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Attachment import Attachment

@dataclass
class AttachmentPublicRead:
  uuid: Optional[str]
  created: Optional[str]
  updated: Optional[str]
  attachment: Optional[Attachment]
