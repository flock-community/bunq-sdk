from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class MonetaryAccountBudget:
  all_category: 'List[str]'
  amount: 'Amount'
  recurrence_type: 'str'
  monetary_account_source_funding_id: 'int'
  payment_day_of_month: 'Optional[int]'

from ..model.Amount import Amount