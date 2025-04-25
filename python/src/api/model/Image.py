from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class Image:
  attachment_public_uuid: 'Optional[str]'
  content_type: 'Optional[str]'
  height: 'Optional[int]'
  width: 'Optional[int]'

