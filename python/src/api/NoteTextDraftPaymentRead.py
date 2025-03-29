from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class NoteTextDraftPaymentRead:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  label_user_creator: 'Optional[LabelUser]'
  content: 'Optional[str]'

from .LabelUser import LabelUser