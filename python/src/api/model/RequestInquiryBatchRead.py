from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class RequestInquiryBatchRead:
  request_inquiries: 'Optional[List[RequestInquiry]]'
  total_amount_inquired: 'Optional[Amount]'
  reference_split_the_bill: 'Optional[RequestReferenceSplitTheBillAnchorObject]'

from ..model.RequestInquiry import RequestInquiry
from ..model.Amount import Amount
from ..model.RequestReferenceSplitTheBillAnchorObject import RequestReferenceSplitTheBillAnchorObject