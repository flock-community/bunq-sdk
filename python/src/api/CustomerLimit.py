from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Amount import Amount

@dataclass
class CustomerLimit:
  limit_monetary_account: Optional[int]
  limit_monetary_account_remaining: Optional[int]
  limit_card_debit_maestro: Optional[int]
  limit_card_debit_mastercard: Optional[int]
  limit_card_debit_wildcard: Optional[int]
  limit_card_wildcard: Optional[int]
  limit_card_replacement: Optional[int]
  limit_amount_monthly: Optional[Amount]
  spent_amount_monthly: Optional[Amount]
