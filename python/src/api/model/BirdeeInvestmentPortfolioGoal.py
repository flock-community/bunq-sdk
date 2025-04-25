from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class BirdeeInvestmentPortfolioGoal:
  amount_target: 'Optional[Amount]'
  time_end: 'Optional[str]'

from ..model.Amount import Amount