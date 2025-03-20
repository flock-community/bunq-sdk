from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .LabelUser import LabelUser
from .DraftPaymentResponse import DraftPaymentResponse
from .DraftPaymentEntry import DraftPaymentEntry
from .DraftPaymentAnchorObject import DraftPaymentAnchorObject
from .RequestInquiryReference import RequestInquiryReference
from .Schedule import Schedule

@dataclass
class DraftPaymentListing:
  id: Optional[int]
  monetary_account_id: Optional[int]
  user_alias_created: Optional[LabelUser]
  responses: Optional[List[DraftPaymentResponse]]
  status: Optional[str]
  type: Optional[str]
  entries: Optional[List[DraftPaymentEntry]]
  object: Optional[DraftPaymentAnchorObject]
  request_reference_split_the_bill: Optional[List[RequestInquiryReference]]
  schedule: Optional[Schedule]
