from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class CurrencyCloudBeneficiaryListing:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  name: 'Optional[str]'
  account_number: 'Optional[str]'
  currency: 'Optional[str]'
  external_identifier: 'Optional[str]'

