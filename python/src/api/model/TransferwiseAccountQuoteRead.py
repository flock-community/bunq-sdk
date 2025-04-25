from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class TransferwiseAccountQuoteRead:
  account_id: 'Optional[str]'
  currency: 'Optional[str]'
  country: 'Optional[str]'
  name_account_holder: 'Optional[str]'
  account_number: 'Optional[str]'
  bank_code: 'Optional[str]'

