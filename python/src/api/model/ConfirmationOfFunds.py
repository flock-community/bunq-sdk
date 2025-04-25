from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class ConfirmationOfFunds:
  pointer_iban: 'Pointer'
  amount: 'Amount'

from ..model.Pointer import Pointer
from ..model.Amount import Amount