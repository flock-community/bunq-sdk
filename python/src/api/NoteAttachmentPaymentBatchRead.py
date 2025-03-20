from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .LabelUser import LabelUser
from .AttachmentMonetaryAccountPayment import AttachmentMonetaryAccountPayment

@dataclass
class NoteAttachmentPaymentBatchRead:
  id: Optional[int]
  created: Optional[str]
  updated: Optional[str]
  label_user_creator: Optional[LabelUser]
  description: Optional[str]
  attachment: Optional[List[AttachmentMonetaryAccountPayment]]
