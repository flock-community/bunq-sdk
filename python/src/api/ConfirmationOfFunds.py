from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Pointer import Pointer
from .Amount import Amount

@dataclass
class ConfirmationOfFunds:
  pointer_iban: Pointer
  amount: Amount
