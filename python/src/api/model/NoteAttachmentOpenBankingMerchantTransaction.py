from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class NoteAttachmentOpenBankingMerchantTransaction:
  description: 'Optional[str]'
  attachment_id: 'int'

