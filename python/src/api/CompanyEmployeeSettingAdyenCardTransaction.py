from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class CompanyEmployeeSettingAdyenCardTransaction:
  pointer_counter_user: 'Pointer'
  status: 'Optional[str]'
  monetary_account_payout_id: 'Optional[int]'

from .Pointer import Pointer