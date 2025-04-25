from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class RequestResponseListing:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  time_responded: 'Optional[str]'
  time_expiry: 'Optional[str]'
  time_refund_requested: 'Optional[str]'
  time_refunded: 'Optional[str]'
  user_refund_requested: 'Optional[LabelUser]'
  monetary_account_id: 'Optional[int]'
  amount_inquired: 'Optional[Amount]'
  amount_responded: 'Optional[Amount]'
  status: 'Optional[str]'
  description: 'Optional[str]'
  alias: 'Optional[LabelMonetaryAccount]'
  counterparty_alias: 'Optional[LabelMonetaryAccount]'
  attachment: 'Optional[List[Attachment]]'
  minimum_age: 'Optional[int]'
  require_address: 'Optional[str]'
  geolocation: 'Optional[Geolocation]'
  type: 'Optional[str]'
  sub_type: 'Optional[str]'
  redirect_url: 'Optional[str]'
  address_billing: 'Optional[Address]'
  address_shipping: 'Optional[Address]'
  credit_scheme_identifier: 'Optional[str]'
  mandate_identifier: 'Optional[str]'
  registration_action: 'Optional[str]'
  eligible_whitelist_id: 'Optional[int]'
  request_reference_split_the_bill: 'Optional[List[RequestInquiryReference]]'
  event_id: 'Optional[int]'
  monetary_account_preferred_id: 'Optional[int]'

from ..model.LabelUser import LabelUser
from ..model.Amount import Amount
from ..model.LabelMonetaryAccount import LabelMonetaryAccount
from ..model.Attachment import Attachment
from ..model.Geolocation import Geolocation
from ..model.Address import Address
from ..model.RequestInquiryReference import RequestInquiryReference