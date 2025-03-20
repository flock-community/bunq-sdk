from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .LabelUser import LabelUser

@dataclass
class NoteTextOpenBankingMerchantTransactionRead:
  id: Optional[int]
  created: Optional[str]
  updated: Optional[str]
  label_user_creator: Optional[LabelUser]
  content: Optional[str]
