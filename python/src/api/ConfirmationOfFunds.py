from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class ConfirmationOfFunds:
  pointer_iban: 'Pointer'
  amount: 'Amount'

from .Pointer import Pointer
from .Amount import Amount