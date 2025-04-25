from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class AttachmentPublicRead:
  uuid: 'Optional[str]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  attachment: 'Optional[Attachment]'

from ..model.Attachment import Attachment