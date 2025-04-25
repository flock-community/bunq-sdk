from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class PaymentServiceProviderIssuerTransactionListing:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  public_uuid: 'Optional[str]'
  counterparty_alias: 'Optional[LabelMonetaryAccount]'
  amount: 'Optional[Amount]'
  description: 'Optional[str]'
  url_redirect: 'Optional[str]'
  time_expiry: 'Optional[str]'
  status: 'Optional[str]'
  alias: 'Optional[LabelMonetaryAccount]'

from ..model.LabelMonetaryAccount import LabelMonetaryAccount
from ..model.Amount import Amount