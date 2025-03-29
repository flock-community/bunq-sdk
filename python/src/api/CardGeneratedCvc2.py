from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class CardGeneratedCvc2:
  type: 'Optional[str]'

