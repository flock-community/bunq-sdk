from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class NoteAttachmentPayment:
  description: 'Optional[str]'
  attachment_id: 'int'

