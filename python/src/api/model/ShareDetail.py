from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class ShareDetail:
  payment: 'Optional[ShareDetailPayment]'
  read_only: 'Optional[ShareDetailReadOnly]'
  draft_payment: 'Optional[ShareDetailDraftPayment]'

from ..model.ShareDetailPayment import ShareDetailPayment
from ..model.ShareDetailReadOnly import ShareDetailReadOnly
from ..model.ShareDetailDraftPayment import ShareDetailDraftPayment