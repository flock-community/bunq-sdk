from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class WhitelistSddRecurring:
  monetary_account_paying_id: 'int'
  request_id: 'int'
  maximum_amount_per_month: 'Optional[Amount]'
  maximum_amount_per_payment: 'Optional[Amount]'
  routing_type: 'Optional[str]'

from ..model.Amount import Amount