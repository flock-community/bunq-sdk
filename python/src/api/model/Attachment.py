from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class Attachment:
  description: 'Optional[str]'
  content_type: 'Optional[str]'
  urls: 'Optional[List[AttachmentUrl]]'

from ..model.AttachmentUrl import AttachmentUrl