from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .LabelUser import LabelUser

@dataclass
class CoOwner:
  alias: Optional[LabelUser]
  status: Optional[str]
