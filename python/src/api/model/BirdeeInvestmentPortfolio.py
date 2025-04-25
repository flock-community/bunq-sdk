from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class BirdeeInvestmentPortfolio:
  risk_profile_type: 'Optional[str]'
  investment_theme: 'Optional[str]'
  name: 'Optional[str]'
  goal: 'Optional[BirdeeInvestmentPortfolioGoal]'
  status: 'Optional[str]'
  number_of_strategy_change_annual_maximum: 'Optional[int]'
  number_of_strategy_change_annual_used: 'Optional[int]'
  external_identifier: 'Optional[str]'
  balance: 'Optional[BirdeeInvestmentPortfolioBalance]'
  allocations: 'Optional[List[BirdeePortfolioAllocation]]'

from ..model.BirdeeInvestmentPortfolioGoal import BirdeeInvestmentPortfolioGoal
from ..model.BirdeeInvestmentPortfolioBalance import BirdeeInvestmentPortfolioBalance
from ..model.BirdeePortfolioAllocation import BirdeePortfolioAllocation