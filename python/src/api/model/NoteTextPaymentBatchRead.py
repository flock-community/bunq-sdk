from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class NoteTextPaymentBatchRead:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  label_user_creator: 'Optional[LabelUser]'
  content: 'Optional[str]'

from ..model.LabelUser import LabelUser