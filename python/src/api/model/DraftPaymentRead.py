from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class DraftPaymentRead:
  id: 'Optional[int]'
  monetary_account_id: 'Optional[int]'
  user_alias_created: 'Optional[LabelUser]'
  responses: 'Optional[List[DraftPaymentResponse]]'
  status: 'Optional[str]'
  type: 'Optional[str]'
  entries: 'Optional[List[DraftPaymentEntry]]'
  object: 'Optional[DraftPaymentAnchorObject]'
  request_reference_split_the_bill: 'Optional[List[RequestInquiryReference]]'
  schedule: 'Optional[Schedule]'

from ..model.LabelUser import LabelUser
from ..model.DraftPaymentResponse import DraftPaymentResponse
from ..model.DraftPaymentEntry import DraftPaymentEntry
from ..model.DraftPaymentAnchorObject import DraftPaymentAnchorObject
from ..model.RequestInquiryReference import RequestInquiryReference
from ..model.Schedule import Schedule