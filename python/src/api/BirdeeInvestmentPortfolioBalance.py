from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Amount import Amount

@dataclass
class BirdeeInvestmentPortfolioBalance:
  amount_available: Optional[Amount]
  amount_deposit_total: Optional[Amount]
  amount_withdrawal_total: Optional[Amount]
  amount_fee_total: Optional[Amount]
  amount_profit: Optional[Amount]
  amount_deposit_pending: Optional[Amount]
  amount_withdrawal_pending: Optional[Amount]
