from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class CurrencyCloudPaymentQuote:
  pointers: 'List[Pointer]'

from ..model.Pointer import Pointer