from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class RequestResponse:
  amount_responded: 'Optional[Amount]'
  status: 'Optional[str]'
  address_shipping: 'Optional[Address]'
  address_billing: 'Optional[Address]'
  currency_conversion_quote_id: 'Optional[int]'
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
  credit_scheme_identifier: 'Optional[str]'
  mandate_identifier: 'Optional[str]'
  registration_action: 'Optional[str]'
  eligible_whitelist_id: 'Optional[int]'
  request_reference_split_the_bill: 'Optional[List[RequestInquiryReference]]'
  event_id: 'Optional[int]'
  monetary_account_preferred_id: 'Optional[int]'

from ..model.Amount import Amount
from ..model.Address import Address
from ..model.LabelUser import LabelUser
from ..model.LabelMonetaryAccount import LabelMonetaryAccount
from ..model.Attachment import Attachment
from ..model.Geolocation import Geolocation
from ..model.RequestInquiryReference import RequestInquiryReference