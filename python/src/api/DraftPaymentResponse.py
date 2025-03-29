from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class DraftPaymentResponse:
  status: 'Optional[str]'
  user_alias_created: 'Optional[LabelUser]'

from .LabelUser import LabelUser