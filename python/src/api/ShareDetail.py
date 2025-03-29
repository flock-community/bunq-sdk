from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class ShareDetail:
  payment: 'Optional[ShareDetailPayment]'
  read_only: 'Optional[ShareDetailReadOnly]'
  draft_payment: 'Optional[ShareDetailDraftPayment]'

from .ShareDetailPayment import ShareDetailPayment
from .ShareDetailReadOnly import ShareDetailReadOnly
from .ShareDetailDraftPayment import ShareDetailDraftPayment