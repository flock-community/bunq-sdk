from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class BirdeeInvestmentPortfolioGoal:
  amount_target: 'Optional[Amount]'
  time_end: 'Optional[str]'

from .Amount import Amount