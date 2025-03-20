from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class NoteAttachmentMasterCardAction:
  description: str
  attachment_id: int
