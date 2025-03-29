from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class OpenBankingAccount:
  status: 'Optional[str]'
  iban: 'Optional[str]'
  time_synced_last: 'Optional[str]'
  provider_bank: 'Optional[OpenBankingProviderBank]'
  balance_booked: 'Optional[Amount]'
  balance_available: 'Optional[Amount]'

from .OpenBankingProviderBank import OpenBankingProviderBank
from .Amount import Amount