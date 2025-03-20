from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .RequestInquiry import RequestInquiry
from .Amount import Amount
from .RequestReferenceSplitTheBillAnchorObject import RequestReferenceSplitTheBillAnchorObject

@dataclass
class RequestInquiryBatchRead:
  request_inquiries: Optional[List[RequestInquiry]]
  total_amount_inquired: Optional[Amount]
  reference_split_the_bill: Optional[RequestReferenceSplitTheBillAnchorObject]
