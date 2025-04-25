from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class TokenQrRequestIdealCreate:
  id: 'Optional[int]'
  time_responded: 'Optional[str]'
  time_expiry: 'Optional[str]'
  monetary_account_id: 'Optional[int]'
  amount_inquired: 'Optional[Amount]'
  amount_responded: 'Optional[Amount]'
  alias: 'Optional[LabelMonetaryAccount]'
  counterparty_alias: 'Optional[LabelMonetaryAccount]'
  description: 'Optional[str]'
  attachment: 'Optional[List[Attachment]]'
  status: 'Optional[str]'
  minimum_age: 'Optional[int]'
  require_address: 'Optional[str]'
  address_shipping: 'Optional[Address]'
  address_billing: 'Optional[Address]'
  geolocation: 'Optional[Geolocation]'
  redirect_url: 'Optional[str]'
  type: 'Optional[str]'
  sub_type: 'Optional[str]'
  eligible_whitelist_id: 'Optional[int]'

from ..model.Amount import Amount
from ..model.LabelMonetaryAccount import LabelMonetaryAccount
from ..model.Attachment import Attachment
from ..model.Address import Address
from ..model.Geolocation import Geolocation