from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .AttachmentUrl import AttachmentUrl

@dataclass
class Attachment:
  description: Optional[str]
  content_type: Optional[str]
  urls: Optional[List[AttachmentUrl]]
