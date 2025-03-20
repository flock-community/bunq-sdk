from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .BirdeeInvestmentPortfolioGoal import BirdeeInvestmentPortfolioGoal
from .BirdeeInvestmentPortfolioBalance import BirdeeInvestmentPortfolioBalance
from .BirdeePortfolioAllocation import BirdeePortfolioAllocation

@dataclass
class BirdeeInvestmentPortfolio:
  risk_profile_type: Optional[str]
  investment_theme: Optional[str]
  name: Optional[str]
  goal: Optional[BirdeeInvestmentPortfolioGoal]
  status: Optional[str]
  number_of_strategy_change_annual_maximum: Optional[int]
  number_of_strategy_change_annual_used: Optional[int]
  external_identifier: Optional[str]
  balance: Optional[BirdeeInvestmentPortfolioBalance]
  allocations: Optional[List[BirdeePortfolioAllocation]]
