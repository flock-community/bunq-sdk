from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class NoteTextBankSwitchServiceNetherlandsIncomingPayment:
  content: 'Optional[str]'

