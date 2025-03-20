from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .ShareDetailPayment import ShareDetailPayment
from .ShareDetailReadOnly import ShareDetailReadOnly
from .ShareDetailDraftPayment import ShareDetailDraftPayment

@dataclass
class ShareDetail:
  payment: Optional[ShareDetailPayment]
  read_only: Optional[ShareDetailReadOnly]
  draft_payment: Optional[ShareDetailDraftPayment]
