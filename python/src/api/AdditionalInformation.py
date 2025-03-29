from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class AdditionalInformation:
  category: 'Optional[str]'
  reason: 'Optional[str]'
  comment: 'Optional[str]'
  attachment: 'Optional[List[AttachmentMasterCardActionRefund]]'
  terms_and_conditions: 'Optional[str]'

from .AttachmentMasterCardActionRefund import AttachmentMasterCardActionRefund