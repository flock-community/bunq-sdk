from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class Attachment:
  description: 'Optional[str]'
  content_type: 'Optional[str]'
  urls: 'Optional[List[AttachmentUrl]]'

from .AttachmentUrl import AttachmentUrl