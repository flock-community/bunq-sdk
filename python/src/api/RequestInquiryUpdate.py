from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class RequestInquiryUpdate:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  time_responded: 'Optional[str]'
  time_expiry: 'Optional[str]'
  monetary_account_id: 'Optional[int]'
  amount_inquired: 'Optional[Amount]'
  amount_responded: 'Optional[Amount]'
  user_alias_created: 'Optional[LabelUser]'
  user_alias_revoked: 'Optional[LabelUser]'
  counterparty_alias: 'Optional[LabelMonetaryAccount]'
  description: 'Optional[str]'
  merchant_reference: 'Optional[str]'
  attachment: 'Optional[List[BunqId]]'
  status: 'Optional[str]'
  batch_id: 'Optional[int]'
  scheduled_id: 'Optional[int]'
  minimum_age: 'Optional[int]'
  require_address: 'Optional[str]'
  address_shipping: 'Optional[Address]'
  address_billing: 'Optional[Address]'
  geolocation: 'Optional[Geolocation]'
  reference_split_the_bill: 'Optional[RequestReferenceSplitTheBillAnchorObject]'

from .Amount import Amount
from .LabelUser import LabelUser
from .LabelMonetaryAccount import LabelMonetaryAccount
from .BunqId import BunqId
from .Address import Address
from .Geolocation import Geolocation
from .RequestReferenceSplitTheBillAnchorObject import RequestReferenceSplitTheBillAnchorObject