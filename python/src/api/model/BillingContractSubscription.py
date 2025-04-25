from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class BillingContractSubscription:
  subscription_type: 'Optional[str]'
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  contract_date_start: 'Optional[str]'
  contract_date_end: 'Optional[str]'
  contract_version: 'Optional[int]'
  subscription_type_downgrade: 'Optional[str]'
  status: 'Optional[str]'
  sub_status: 'Optional[str]'

