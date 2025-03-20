from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .LabelUser import LabelUser

@dataclass
class DraftPaymentResponse:
  status: Optional[str]
  user_alias_created: Optional[LabelUser]
