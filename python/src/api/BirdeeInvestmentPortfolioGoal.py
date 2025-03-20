from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Amount import Amount

@dataclass
class BirdeeInvestmentPortfolioGoal:
  amount_target: Optional[Amount]
  time_end: Optional[str]
