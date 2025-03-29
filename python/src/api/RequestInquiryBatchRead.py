from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class RequestInquiryBatchRead:
  request_inquiries: 'Optional[List[RequestInquiry]]'
  total_amount_inquired: 'Optional[Amount]'
  reference_split_the_bill: 'Optional[RequestReferenceSplitTheBillAnchorObject]'

from .RequestInquiry import RequestInquiry
from .Amount import Amount
from .RequestReferenceSplitTheBillAnchorObject import RequestReferenceSplitTheBillAnchorObject