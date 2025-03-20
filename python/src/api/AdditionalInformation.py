from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .AttachmentMasterCardActionRefund import AttachmentMasterCardActionRefund

@dataclass
class AdditionalInformation:
  category: Optional[str]
  reason: Optional[str]
  comment: Optional[str]
  attachment: Optional[List[AttachmentMasterCardActionRefund]]
  terms_and_conditions: Optional[str]
