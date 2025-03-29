from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class BillingContractSubscriptionListing:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  contract_date_start: 'Optional[str]'
  contract_date_end: 'Optional[str]'
  contract_version: 'Optional[int]'
  subscription_type: 'Optional[str]'
  subscription_type_downgrade: 'Optional[str]'
  status: 'Optional[str]'
  sub_status: 'Optional[str]'

