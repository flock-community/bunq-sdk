from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class RequestInquiryBatch:
  request_inquiries: 'Optional[List[RequestInquiry]]'
  status: 'Optional[str]'
  total_amount_inquired: 'Optional[Amount]'
  event_id: 'Optional[int]'
  reference_split_the_bill: 'Optional[RequestReferenceSplitTheBillAnchorObject]'

from ..model.RequestInquiry import RequestInquiry
from ..model.Amount import Amount
from ..model.RequestReferenceSplitTheBillAnchorObject import RequestReferenceSplitTheBillAnchorObject