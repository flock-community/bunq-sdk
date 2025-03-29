from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class CoOwner:
  alias: 'Optional[LabelUser]'
  status: 'Optional[str]'

from .LabelUser import LabelUser