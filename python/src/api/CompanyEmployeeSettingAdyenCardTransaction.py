from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Pointer import Pointer

@dataclass
class CompanyEmployeeSettingAdyenCardTransaction:
  pointer_counter_user: Pointer
  status: Optional[str]
  monetary_account_payout_id: Optional[int]
