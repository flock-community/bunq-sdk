from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class WhitelistResult:
  id: 'Optional[int]'
  monetary_account_paying_id: 'Optional[int]'
  status: 'Optional[str]'
  sub_status: 'Optional[str]'
  error_message: 'Optional[List[List[ErrorArray]]]'
  whitelist: 'Optional[Whitelist]'
  object: 'Optional[WhitelistResultViewAnchoredObject]'
  request_reference_split_the_bill: 'Optional[List[RequestInquiryReference]]'

from ..model.ErrorArray import ErrorArray
from ..model.Whitelist import Whitelist
from ..model.WhitelistResultViewAnchoredObject import WhitelistResultViewAnchoredObject
from ..model.RequestInquiryReference import RequestInquiryReference