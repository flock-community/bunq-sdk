from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class DraftPaymentResponse:
  status: 'Optional[str]'
  user_alias_created: 'Optional[LabelUser]'

from ..model.LabelUser import LabelUser