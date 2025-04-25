from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class NoteAttachmentPaymentRead:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  label_user_creator: 'Optional[LabelUser]'
  description: 'Optional[str]'
  attachment: 'Optional[List[AttachmentMonetaryAccountPayment]]'

from ..model.LabelUser import LabelUser
from ..model.AttachmentMonetaryAccountPayment import AttachmentMonetaryAccountPayment