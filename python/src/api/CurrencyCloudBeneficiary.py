from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class CurrencyCloudBeneficiary:
  name: 'str'
  country: 'str'
  currency: 'str'
  payment_type: 'str'
  legal_entity_type: 'str'
  all_field: 'List[str]'

