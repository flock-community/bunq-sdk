from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class RequestInquiry:
  amount_inquired: 'Optional[Amount]'
  counterparty_alias: 'Optional[LabelMonetaryAccount]'
  description: 'Optional[str]'
  attachment: 'Optional[List[BunqId]]'
  merchant_reference: 'Optional[str]'
  status: 'Optional[str]'
  minimum_age: 'Optional[int]'
  require_address: 'Optional[str]'
  want_tip: 'Optional[bool]'
  allow_amount_lower: 'Optional[bool]'
  allow_amount_higher: 'Optional[bool]'
  allow_bunqme: 'bool'
  redirect_url: 'Optional[str]'
  event_id: 'Optional[int]'
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  time_responded: 'Optional[str]'
  time_expiry: 'Optional[str]'
  monetary_account_id: 'Optional[int]'
  amount_responded: 'Optional[Amount]'
  user_alias_created: 'Optional[LabelUser]'
  user_alias_revoked: 'Optional[LabelUser]'
  batch_id: 'Optional[int]'
  scheduled_id: 'Optional[int]'
  bunqme_share_url: 'Optional[str]'
  address_shipping: 'Optional[Address]'
  address_billing: 'Optional[Address]'
  geolocation: 'Optional[Geolocation]'
  reference_split_the_bill: 'Optional[RequestReferenceSplitTheBillAnchorObject]'

from ..model.Amount import Amount
from ..model.LabelMonetaryAccount import LabelMonetaryAccount
from ..model.BunqId import BunqId
from ..model.LabelUser import LabelUser
from ..model.Address import Address
from ..model.Geolocation import Geolocation
from ..model.RequestReferenceSplitTheBillAnchorObject import RequestReferenceSplitTheBillAnchorObject