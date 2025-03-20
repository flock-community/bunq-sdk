from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Amount import Amount
from .CardCountryPermission import CardCountryPermission

@dataclass
class CardBatchEntry:
  id: int
  status: Optional[str]
  card_limit: Optional[Amount]
  card_limit_atm: Optional[Amount]
  country_permission: Optional[List[CardCountryPermission]]
  monetary_account_id_fallback: Optional[int]
